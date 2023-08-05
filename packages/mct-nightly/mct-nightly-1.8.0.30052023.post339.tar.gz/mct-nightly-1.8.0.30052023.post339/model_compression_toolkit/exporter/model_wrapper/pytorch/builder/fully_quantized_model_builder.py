# Copyright 2022 Sony Semiconductor Israel, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from model_compression_toolkit.core import common
from model_compression_toolkit.core.common import Graph
from model_compression_toolkit.constants import FOUND_TORCH
from model_compression_toolkit.logger import Logger

if FOUND_TORCH:
    import torch
    from mct_quantizers import PytorchQuantizationWrapper
    from model_compression_toolkit.core.pytorch.back2framework.pytorch_model_builder import PyTorchModelBuilder
    from model_compression_toolkit.exporter.model_wrapper.pytorch.builder.node_to_quantizers import \
        get_quantization_quantizers

    def fully_quantized_wrapper(node: common.BaseNode,
                                module: torch.nn.Module) -> PytorchQuantizationWrapper:
        """
        A function which takes a computational graph node and a pytorch module and
        perform the quantization wrapping

        Args:
            node: A node of mct graph.
            module: A Pytorch module
        Returns: Wrapped layer

        """
        weight_quantizers, activation_quantizers = get_quantization_quantizers(node)
        wrapped_layer = PytorchQuantizationWrapper(module, weight_quantizers, activation_quantizers)
        return wrapped_layer


    def get_exportable_pytorch_model(graph: Graph):
        """
        Convert graph to fully quantized PyTorch model.

        Args:
            graph: Graph to convert to a PyTorch model.

        Returns:
            Fully quantized PyTorch model.
        """
        return PyTorchModelBuilder(graph=graph,
                                   wrapper=fully_quantized_wrapper).build_model()
else:
    def get_exportable_pytorch_model(*args, **kwargs):  # pragma: no cover
        Logger.error('Installing torch is mandatory '
                     'when using get_exportable_pytorch_model. '
                     'Could not find PyTorch package.')