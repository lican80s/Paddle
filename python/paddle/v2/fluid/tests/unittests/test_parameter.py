#   Copyright (c) 2018 PaddlePaddle Authors. All Rights Reserved.
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

import unittest
from paddle.v2.fluid.framework import default_main_program
import paddle.v2.fluid.core as core
from paddle.v2.fluid.executor import Executor
import paddle.v2.fluid.io as io
from paddle.v2.fluid.initializer import ConstantInitializer
import numpy as np

main_program = default_main_program()


class TestParameter(unittest.TestCase):
    def test_param(self):
        shape = [784, 100]
        val = 1.0625
        b = main_program.global_block()
        param = b.create_parameter(
            name='fc.w',
            shape=shape,
            dtype='float32',
            initializer=ConstantInitializer(val))
        self.assertIsNotNone(param)
        self.assertEqual('fc.w', param.name)
        self.assertEqual((784, 100), param.shape)
        self.assertEqual(core.VarDesc.VarType.FP32, param.dtype)
        self.assertEqual(0, param.block.idx)
        exe = Executor(core.CPUPlace())
        p = exe.run(main_program, fetch_list=[param])[0]
        self.assertTrue(np.allclose(p, np.ones(shape) * val))
        p = io.get_parameter_value_by_name('fc.w', exe, main_program)
        self.assertTrue(np.allclose(np.array(p), np.ones(shape) * val))


if __name__ == '__main__':
    unittest.main()
