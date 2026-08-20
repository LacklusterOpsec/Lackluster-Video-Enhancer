"""
MIT License

Copyright (c) 2021 HolyWu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import torch
import torch.nn.functional as F


def warp(tenInput, tenFlow, tenFlow_div, backwarp_tenGrid):
    dtype = tenInput.dtype
    if dtype != torch.float16:
        # fp32/bf16: compute in fp32 for precision (matches upstream RIFE)
        tenInput = tenInput.to(torch.float)
        tenFlow = tenFlow.to(torch.float)

    tenFlow = torch.cat(
        [tenFlow[:, 0:1] / tenFlow_div[0], tenFlow[:, 1:2] / tenFlow_div[1]], 1
    )
    g = (backwarp_tenGrid + tenFlow).permute(0, 2, 3, 1)

    if dtype == torch.float16:
        # keep the whole grid_sample in fp16 - the fp32-cast-then-downcast
        # pattern is what triggers incorrect output in mixed-precision TRT
        # engines (pytorch/TensorRT#4074); fp16-only is the known-good path
        # used by ComfyUI-Rife-Tensorrt
        g = g.half()
        tenInput = tenInput.half()
        backwarp_tenGrid16 = backwarp_tenGrid.half() if backwarp_tenGrid.dtype != torch.float16 else backwarp_tenGrid
        g = (backwarp_tenGrid16 + tenFlow).permute(0, 2, 3, 1)
        pd = 'border'
        if tenInput.device.type == "mps":
            pd = 'zeros'
            g = g.clamp(-1, 1)
        return F.grid_sample(input=tenInput, grid=g, mode="bilinear", padding_mode=pd, align_corners=True)

    pd = 'border'
    if tenInput.device.type == "mps":
        pd = 'zeros'
        g = g.clamp(-1, 1)
    return F.grid_sample(input=tenInput, grid=g, mode="bilinear", padding_mode=pd, align_corners=True).to(dtype)
