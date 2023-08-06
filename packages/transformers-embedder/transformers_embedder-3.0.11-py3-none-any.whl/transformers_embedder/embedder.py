from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union, Tuple, Sequence, Any, Mapping

import transformers as tr

from transformers_embedder import utils
from transformers_embedder.modules.scalar_mix import ScalarMix
from transformers_embedder.modules.encoder import Encoder

if utils.is_torch_available():
    import torch

logger = utils.get_logger(__name__)
utils.get_logger("transformers")


@dataclass
class TransformersEmbedderOutput(tr.file_utils.ModelOutput):
    """Class for model's outputs."""

    word_embeddings: Optional[torch.FloatTensor] = None
    last_hidden_state: Optional[torch.FloatTensor] = None
    pooler_output: Optional[torch.FloatTensor] = None
    hidden_states: Optional[Tuple[torch.FloatTensor]] = None
    attentions: Optional[Tuple[torch.FloatTensor]] = None


class TransformersEmbedder(torch.nn.Module):
    """
    Transformer Embedder class.

    Word level embeddings from various transformer architectures from Huggingface Transformers API.

    Args:
        model (`str`, `tr.PreTrainedModel`):
            Transformer model to use (https://huggingface.co/models).
        layer_pooling_strategy (`str`, optional, defaults to `last`):
            What output to get from the transformer model. The last hidden state (``last``),
            the concatenation of the selected hidden layers (``concat``), the sum of the selected hidden
            layers (``sum``), the average of the selected hidden layers (``mean``), or a scalar mixture of
            the selected hidden layers (``scalar_mix``).
        subword_pooling_strategy (`str`, optional, defaults to `sparse`):
            What pooling strategy to use for the sub-word embeddings. Methods available are ``sparse``,
            ``scatter`` and ``none``. The ``scatter`` strategy is ONNX comptabile but uses ``scatter_add_``
            that is not deterministic. The ``sparse`` strategy is deterministic but it is not comptabile
            with ONNX. When ``subword_pooling_strategy`` is ``none``, the sub-word embeddings are not
            pooled.
        output_layers (`tuple`, `list`, `str`, optional, defaults to `(-4, -3, -2, -1)`):
            Which hidden layers to get from the transformer model. If ``output_layers`` is ``all``,
            all the hidden layers are returned. If ``output_layers`` is a tuple or a list, the hidden
            layers are selected according to the indexes in the tuple or list. If ``output_layers`` is
            a string, it must be ``all``.
        fine_tune (`bool`, optional, defaults to `True`):
            If ``True``, the transformer model is fine-tuned during training.
        return_all (`bool`, optional, defaults to `False`):
            If ``True``, returns all the outputs from the HuggingFace model.
        from_pretrained (`bool`, optional, defaults to `True`):
            If ``True``, the model is loaded from a pre-trained model, otherwise it is initialized with
            random weights. Usefull when you want to load a model from a specific checkpoint, without
            having to download the entire model.
    """

    def __init__(
        self,
        model: Union[str, tr.PreTrainedModel],
        layer_pooling_strategy: str = "last",
        subword_pooling_strategy: str = "scatter",
        output_layers: Union[Sequence[int], str] = (-4, -3, -2, -1),
        fine_tune: bool = True,
        return_all: bool = False,
        from_pretrained: bool = True,
        *args,
        **kwargs,
    ) -> None:
        super().__init__()
        if isinstance(model, str):
            self.config = tr.AutoConfig.from_pretrained(
                model,
                output_hidden_states=True,
                output_attentions=True,
                *args,
                **kwargs,
            )
            if from_pretrained:
                self.transformer_model = tr.AutoModel.from_pretrained(
                    model, config=self.config, *args, **kwargs
                )
            else:
                self.transformer_model = tr.AutoModel.from_config(
                    self.config, *args, **kwargs
                )
        else:
            self.transformer_model = model

        # pooling strategy parameters
        self.layer_pooling_strategy = layer_pooling_strategy
        self.subword_pooling_strategy = subword_pooling_strategy

        if output_layers == "all":
            output_layers = tuple(
                range(self.transformer_model.config.num_hidden_layers)
            )

        # check output_layers is well defined
        if (
            max(map(abs, output_layers))
            >= self.transformer_model.config.num_hidden_layers
        ):
            raise ValueError(
                f"`output_layers` parameter not valid, choose between 0 and "
                f"{self.transformer_model.config.num_hidden_layers - 1}. "
                f"Current value is `{output_layers}`"
            )
        self.output_layers = output_layers

        self._scalar_mix: Optional[ScalarMix] = None
        if layer_pooling_strategy == "scalar_mix":
            self._scalar_mix = ScalarMix(len(output_layers))

        # check if return all transformer outputs
        self.return_all = return_all

        # if fine_tune is False, freeze all the transformer's parameters
        if not fine_tune:
            for param in self.transformer_model.parameters():
                param.requires_grad = False

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        token_type_ids: Optional[torch.Tensor] = None,
        scatter_offsets: Optional[torch.Tensor] = None,
        sparse_offsets: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ) -> TransformersEmbedderOutput:
        """
        Forward method of the PyTorch module.

        Args:
            input_ids (`torch.Tensor`):
                Input ids for the transformer model.
            attention_mask (`torch.Tensor`, optional):
                Attention mask for the transformer model.
            token_type_ids (`torch.Tensor`, optional):
                Token type ids for the transformer model.
            scatter_offsets (`torch.Tensor`, optional):
                Offsets of the sub-word, used to reconstruct the word embeddings using
                the ``scatter`` method.
            sparse_offsets (`Mapping[str, Any]`, optional):
                Offsets of the sub-word, used to reconstruct the word embeddings using
                the ``sparse`` method.

        Returns:
            `TransformersEmbedderOutput`:
                Word level embeddings plus the output of the transformer model.
        """
        # Some HuggingFace models don't have the
        # token_type_ids parameter and fail even when it's given as None.
        inputs = {"input_ids": input_ids, "attention_mask": attention_mask}
        if token_type_ids is not None:
            inputs["token_type_ids"] = token_type_ids

        # Shape: [batch_size, num_sub-words, embedding_size].
        transformer_outputs = self.transformer_model(**inputs)
        if self.layer_pooling_strategy == "last":
            word_embeddings = transformer_outputs.last_hidden_state
        elif self.layer_pooling_strategy == "concat":
            word_embeddings = [
                transformer_outputs.hidden_states[layer] for layer in self.output_layers
            ]
            word_embeddings = torch.cat(word_embeddings, dim=-1)
        elif self.layer_pooling_strategy == "sum":
            word_embeddings = [
                transformer_outputs.hidden_states[layer] for layer in self.output_layers
            ]
            word_embeddings = torch.stack(word_embeddings, dim=0).sum(dim=0)
        elif self.layer_pooling_strategy == "mean":
            word_embeddings = [
                transformer_outputs.hidden_states[layer] for layer in self.output_layers
            ]
            word_embeddings = torch.stack(word_embeddings, dim=0).mean(
                dim=0, dtype=torch.float
            )
        elif self.layer_pooling_strategy == "scalar_mix":
            word_embeddings = [
                transformer_outputs.hidden_states[layer] for layer in self.output_layers
            ]
            word_embeddings = self._scalar_mix(word_embeddings)
        else:
            raise ValueError(
                "`layer_pooling_strategy` parameter not valid, choose between `last`, `concat`, "
                f"`sum`, `mean` and `scalar_mix`. Current value `{self.layer_pooling_strategy}`"
            )

        if (
            self.subword_pooling_strategy != "none"
            and scatter_offsets is None
            and sparse_offsets is None
        ):
            raise ValueError(
                "`subword_pooling_strategy` is not `none` but neither `scatter_offsets` not `sparse_offsets` "
                "were passed to the model. Cannot compute word embeddings.\nTo solve:\n"
                "- Set `subword_pooling_strategy` to `none` or\n"
                "- Pass `scatter_offsets` to the model during forward or\n"
                "- Pass `sparse_offsets` to the model during forward."
            )

        if self.subword_pooling_strategy not in ["none", "scatter", "sparse"]:
            raise ValueError(
                "`subword_pooling_strategy` parameter not valid, choose between `scatter`, `sparse`"
                f" and `none`. Current value is `{self.subword_pooling_strategy}`."
            )
        if self.subword_pooling_strategy == "scatter":
            if scatter_offsets is None:
                raise ValueError(
                    "`subword_pooling_strategy` is `scatter` but `scatter_offsets` "
                    "were not passed to the model. Cannot compute word embeddings.\nTo solve:\n"
                    "- Set `subword_pooling_strategy` to `none` or\n"
                    "- Pass `scatter_offsets` to the model during forward."
                )
            word_embeddings = self.merge_scatter(
                word_embeddings, indices=scatter_offsets
            )
        if self.subword_pooling_strategy == "sparse":
            if sparse_offsets is None:
                raise ValueError(
                    "`subword_pooling_strategy` is `sparse` but `sparse_offsets` "
                    "were not passed to the model. Cannot compute word embeddings.\nTo solve:\n"
                    "- Set `subword_pooling_strategy` to `none` or\n"
                    "- Pass `sparse_offsets` to the model during forward."
                )
            word_embeddings = self.merge_sparse(word_embeddings, sparse_offsets)

        if self.return_all:
            return TransformersEmbedderOutput(
                word_embeddings=word_embeddings,
                last_hidden_state=transformer_outputs.last_hidden_state,
                hidden_states=transformer_outputs.hidden_states,
                pooler_output=transformer_outputs.pooler_output
                if hasattr(transformer_outputs, "pooler_output")
                else None,
                attentions=transformer_outputs.attentions,
            )
        return TransformersEmbedderOutput(word_embeddings=word_embeddings)

    @staticmethod
    def merge_scatter(embeddings: torch.Tensor, indices: torch.Tensor) -> torch.Tensor:
        """
        Minimal version of ``scatter_mean``, from `pytorch_scatter
        <https://github.com/rusty1s/pytorch_scatter/>`_
        library, that is compatible for ONNX but works only for our case.
        It is used to compute word level embeddings from the transformer output.

        Args:
            embeddings (`torch.Tensor`):
                The embeddings tensor.
            indices (`torch.Tensor`):
                The sub-word indices.

        Returns:
            `torch.Tensor`
        """

        def broadcast(src: torch.Tensor, other: torch.Tensor):
            """
            Broadcast ``src`` to match the shape of ``other``.

            Args:
                src (`torch.Tensor`):
                    The tensor to broadcast.
                other (`torch.Tensor`):
                    The tensor to match the shape of.

            Returns:
                `torch.Tensor`: The broadcasted tensor.
            """
            for _ in range(src.dim(), other.dim()):
                src = src.unsqueeze(-1)
            src = src.expand_as(other)
            return src

        def scatter_sum(src: torch.Tensor, index: torch.Tensor) -> torch.Tensor:
            """
            Sums the elements in ``src`` that have the same indices as in ``index``.

            Args:
                src (`torch.Tensor`):
                    The tensor to sum.
                index (`torch.Tensor`):
                    The indices to sum.

            Returns:
                `torch.Tensor`: The summed tensor.
            """
            index = broadcast(index, src)
            size = list(src.size())
            size[1] = index.max() + 1
            out = torch.zeros(size, dtype=src.dtype, device=src.device)
            return out.scatter_add_(1, index, src)

        # replace padding indices with the maximum value inside the batch
        indices[indices == -1] = torch.max(indices)
        merged = scatter_sum(embeddings, indices)
        ones = torch.ones(
            indices.size(), dtype=embeddings.dtype, device=embeddings.device
        )
        count = scatter_sum(ones, indices)
        count.clamp_(1)
        count = broadcast(count, merged)
        merged.true_divide_(count)
        return merged

    @staticmethod
    def merge_sparse(
        embeddings: torch.Tensor, bpe_info: Optional[Mapping[str, Any]]
    ) -> torch.Tensor:
        """
        Merges the subword embeddings into a single tensor, using sparse indices.

        Args:
            embeddings (`torch.Tensor`):
                The embeddings tensor.
            bpe_info (`Mapping[str, Any]`, `optional`):
                The BPE info.

        Returns:
            `torch.Tensor`: The merged embeddings.
        """
        # it is constructed here and not in the tokenizer/collate because pin_memory is not sparse-compatible
        bpe_weights = torch.sparse_coo_tensor(
            indices=bpe_info["sparse_indices"],
            values=bpe_info["sparse_values"],
            size=bpe_info["sparse_size"],
        )
        # (sentence, word, bpe) x (sentence, bpe, transformer_dim) -> (sentence, word, transformer_dim)
        merged = torch.bmm(bpe_weights.to_dense(), embeddings)
        return merged

    def resize_token_embeddings(
        self, new_num_tokens: Optional[int] = None
    ) -> torch.nn.Embedding:
        """
        Resizes input token embeddings' matrix of the model if `new_num_tokens != config.vocab_size`.

        Args:
            new_num_tokens (`int`):
                The number of new tokens in the embedding matrix.

        Returns:
            `torch.nn.Embedding`: Pointer to the input tokens Embeddings Module of the model.
        """
        return self.transformer_model.resize_token_embeddings(new_num_tokens)

    def save_pretrained(self, save_directory: Union[str, Path]):
        """
        Save a model and its configuration file to a directory.

        Args:
            save_directory (`str`, `Path`):
                Directory to which to save.
        """
        self.transformer_model.save_pretrained(save_directory)

    @property
    def hidden_size(self) -> int:
        """
        Returns the hidden size of TransformersEmbedder.

        Returns:
            `int`: Hidden size of ``self.transformer_model``.
        """
        multiplier = (
            len(self.output_layers) if self.layer_pooling_strategy == "concat" else 1
        )
        return self.transformer_model.config.hidden_size * multiplier

    @property
    def transformer_hidden_size(self) -> int:
        """
        Returns the hidden size of the inner transformer.

        Returns:
            `int`: Hidden size of ``self.transformer_model``.
        """
        multiplier = (
            len(self.output_layers) if self.layer_pooling_strategy == "concat" else 1
        )
        return self.transformer_model.config.hidden_size * multiplier


class TransformersEncoder(TransformersEmbedder):
    """
    Transformer Embedder class.

    Word level embeddings from various transformer architectures from Huggingface Transformers API.

    Args:
        model (`str`, `tr.PreTrainedModel`):
            Transformer model to use (https://huggingface.co/models).
        layer_pooling_strategy (`str`, optional, defaults to `last`):
            What output to get from the transformer model. The last hidden state (``last``),
            the concatenation of the selected hidden layers (``concat``), the sum of the selected hidden
            layers (``sum``), the average of the selected hidden layers (``mean``).
        subword_pooling_strategy (`str`, optional, defaults to `scatter`):
            What pooling strategy to use for the sub-word embeddings. Methods available are ``scatter``,
            ``sparse`` and ``none``. The ``scatter`` strategy is ONNX comptabile but uses ``scatter_add``
            that is not deterministic. The ``sparse`` strategy is deterministic but it is not comptabile
            with ONNX.
        output_layers (`tuple`, optional, defaults to `(-4, -3, -2, -1)`):
            Which hidden layers to get from the transformer model.
        fine_tune (`bool`, optional, defaults to `True`):
            If ``True``, the transformer model is fine-tuned during training.
        return_all (`bool`, optional, defaults to `False`):
            If ``True``, returns all the outputs from the HuggingFace model.
        projection_size (`int`, optional, defaults to `None`):
            If not ``None``, the output of the transformer is projected to this size.
        activation_layer (`torch.nn.Module`, optional, defaults to `None`):
            Activation layer to use. If ``None``, no activation layer is used.
        dropout (`float`, optional, defaults to `0.1`):
            The dropout probability.
        bias (`bool`, optional, defaults to `True`):
            If ``True``, the transformer model has a bias.
    """

    def __init__(
        self,
        model: Union[str, tr.PreTrainedModel],
        layer_pooling_strategy: str = "last",
        subword_pooling_strategy: str = "sparse",
        output_layers: Sequence[int] = (-4, -3, -2, -1),
        fine_tune: bool = True,
        return_all: bool = False,
        projection_size: Optional[int] = None,
        activation_layer: Optional[torch.nn.Module] = None,
        dropout: float = 0.1,
        bias: bool = True,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(
            model,
            layer_pooling_strategy,
            subword_pooling_strategy,
            output_layers,
            fine_tune,
            return_all,
            *args,
            **kwargs,
        )
        self.encoder = Encoder(
            self.transformer_hidden_size,
            projection_size,
            activation_layer,
            dropout,
            bias,
        )

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: Optional[torch.Tensor] = None,
        token_type_ids: Optional[torch.Tensor] = None,
        scatter_offsets: Optional[torch.Tensor] = None,
        sparse_offsets: Optional[Mapping[str, Any]] = None,
        **kwargs,
    ) -> TransformersEmbedderOutput:
        """
        Forward method of the PyTorch module.

        Args:
            input_ids (`torch.Tensor`):
                Input ids for the transformer model.
            attention_mask (`torch.Tensor`, optional):
                Attention mask for the transformer model.
            token_type_ids (`torch.Tensor`, optional):
                Token type ids for the transformer model.
            scatter_offsets (`torch.Tensor`, optional):
                Offsets of the sub-word, used to reconstruct the word embeddings.

        Returns:
            `TransformersEmbedderOutput`:
                Word level embeddings plus the output of the transformer model.
        """
        transformers_kwargs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
            "token_type_ids": token_type_ids,
            "scatter_offsets": scatter_offsets,
            "sparse_offsets": sparse_offsets,
            **kwargs,
        }
        transformer_output = super().forward(**transformers_kwargs)
        encoder_output = self.encoder(transformer_output.word_embeddings)
        transformer_output.word_embeddings = encoder_output
        return transformer_output

    @property
    def hidden_size(self) -> int:
        """
        Returns the hidden size of the transformer.

        Returns:
            `int`: Hidden size of ``self.transformer_model``.
        """
        return self.encoder.projection_size
