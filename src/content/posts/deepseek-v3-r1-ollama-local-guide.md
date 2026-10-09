---
title: "How to Run DeepSeek V3 & R1 Locally with Ollama: Full Mac, Linux & Windows Guide"
description: "In-depth technical breakdown of Run DeepSeek V3 and R1 Locally with Ollama, covering architecture, quantization, hardware benchmarks, and multi-OS deployment."
date: 2026-10-09
categories: ["AI Tools"]
tags: ["DeepSeek", "Ollama", "Local AI", "Open Source", "LLM"]
cover: "/img/posts/deepseek-v3-r1-ollama-local-guide.jpg"
toc: true
home: true
---

The release of DeepSeek-V3 and the reasoning-specialized DeepSeek-R1 marked a watershed moment in open-weight artificial intelligence. Delivering frontier-tier performance that rivals closed-source proprietary systems, DeepSeek’s models leverage cutting-edge architectures—including Multi-Head Latent Attention (MLA) and sparse Mixture-of-Experts (MoE) routing. 

However, running a 671-billion-parameter MoE model or its reasoning-distilled variants in a local development environment introduces significant hardware orchestration, quantization, and runtime challenges. Ollama abstracts the underlying `llama.cpp` runtime into an enterprise-grade local serving layer, making it the premier deployment tool across macOS, Linux, and Windows.

This technical guide unpacks the foundational architecture of DeepSeek-V3 and R1, provides detailed hardware benchmarks, walks through operating-system-specific installation and optimization, and demonstrates production integration via Ollama's API.

---

## Executive Summary & Technical Specifications

| Feature / Metric | DeepSeek-V3 (Base / Chat) | DeepSeek-R1 (Full Reasoning) | DeepSeek-R1 Distilled (Qwen/Llama) |
| :--- | :--- | :--- | :--- |
| **Total Parameters** | 671 Billion | 671 Billion | 1.5B, 7B, 8B, 14B, 32B, 70B |
| **Active Parameters/Token** | 37 Billion (MoE) | 37 Billion (MoE) | Dense (All active) |
| **Attention Architecture** | Multi-Head Latent Attention (MLA) | Multi-Head Latent Attention (MLA) | Standard Multi-Head / GQA |
| **Primary Quantization Format** | FP8 / GGUF (Q4_K_M, Q8_0) | FP8 / GGUF (Q4_K_M, Q8_0) | GGUF (Q4_K_M, Q5_K_M, Q8_0) |
| **Target Context Window** | 64k to 128k Tokens | 64k to 128k Tokens | Up to 128k Tokens (VRAM dependent) |
| **Inference Engine** | Ollama / `llama.cpp` Core | Ollama / `llama.cpp` Core | Ollama Native Engine |
| **Primary Workload Profile** | Massive throughput, multi-turn coding | Extended Chain-of-Thought reasoning | Edge computing, workstations, local agents |

<figure class="my-6">
  <img src="/img/posts/deepseek-v3-r1-ollama-local-guide.jpg" alt="How to Run DeepSeek V3 & R1 Locally with Ollama: Full Mac, Linux & Windows Guide" class="w-full rounded-2xl border border-slate-200 dark:border-slate-700 shadow-md object-cover max-h-[420px]" loading="lazy" />
  <figcaption class="text-xs text-center text-slate-500 dark:text-slate-400 mt-2 italic">
    Architecture & Workflow Overview: How to Run DeepSeek V3 & R1 Locally with Ollama: Full Mac, Linux & Windows Guide
  </figcaption>
</figure>

---

## Architectural Deep Dive: DeepSeek-V3 and R1

To operate these models efficiently, you must understand their underlying compute mechanics and how Ollama parses them.

### Multi-Head Latent Attention (MLA) & DeepSeekMoE
DeepSeek-V3 achieves exceptional inference efficiency through two architectural innovations:
1. **Multi-Head Latent Attention (MLA):** Standard Multi-Head Attention (MHA) creates an unsustainable Key-Value (KV) cache footprint at context lengths exceeding 32k tokens. MLA compresses the KV cache into a low-dimensional latent space using down-projection matrices, cutting memory bandwidth requirements by up to 93% compared to conventional transformer configurations.
2. **DeepSeekMoE:** Unlike dense architectures that activate all parameters on every forward pass, DeepSeek-V3 routes tokens through 256 fine-grained routed experts and 1 shared expert. Only 8 routed experts are activated per token, meaning inference memory access is restricted to approximately 37 billion active parameters while preserving the representational capacity of a 671-billion-parameter network.

Token Input ──► [Input Embedding]
                      │
                      ▼
         [Multi-Head Latent Attention] ──► Compresses KV Cache into Low-Rank Latents
                      │
                      ▼
            [DeepSeekMoE Layer]
         ┌────────────┼────────────┐
         ▼            ▼            ▼
     [Shared Exp] [Routed Exp 1] [Routed Exp 2...8]  (37B Active / 671B Total)
         └────────────┬────────────┘
                      ▼
              Residual Addition ──► Output Latents
### DeepSeek-R1: Reinforcement Learning & Chain-of-Thought
DeepSeek-R1 introduces an autonomous reasoning framework trained via large-scale reinforcement learning (RL) without supervised fine-tuning (SFT) as an initial bottleneck. DeepSeek-R1 constructs explicit, self-verifying, and dynamic `<think>` execution loops before yielding the final response. 

Because the full 671B model requires enterprise multi-GPU nodes even at 4-bit quantization, DeepSeek distilled R1's reasoning traces into dense architectures based on Qwen 2.5 (`1.5b`, `7b`, `14b`, `32b`) and Llama 3.3 (`8b`, `70b`). Ollama exposes these through unified model identifiers, giving developers local access to R1-level logical deduction on standard consumer hardware.

---

## Hardware Benchmarks & Sizing Matrix

Selecting the appropriate parameter size and quantization level depends on available GPU VRAM and system memory bandwidth.

| Model Variant | Minimum RAM/VRAM | Recommended Hardware Setup | Quantization | Tokens/sec (Est.) |
| :--- | :--- | :--- | :--- | :--- |
| **R1 Distill 1.5B** | 4 GB | Base Apple M-Series, GTX 1660 | Q4_K_M | 85–120 tok/s |
| **R1 Distill 7B / 8B** | 8 GB | RTX 3060 (12GB), Apple M1/M2/M3 (16GB) | Q4_K_M | 45–65 tok/s |
| **R1 Distill 14B** | 16 GB | RTX 4070 (12GB + Offload), Apple M-Series (24GB+) | Q4_K_M | 30–45 tok/s |
| **R1 Distill 32B** | 24 GB | RTX 3090/4090 (24GB), Apple M2/M3 Max (36GB+) | Q4_K_M | 20–35 tok/s |
| **R1 Distill 70B** | 48 GB | 2x RTX 3090/4090, Apple M2/M3/M4 Max/Ultra (64GB+) | Q4_K_M | 12–22 tok/s |
| **V3 / R1 Full (671B)** | ~400 GB | 8x H100/A100 (80GB) or Mac Studio Ultra Cluster (512GB) | Q4_K_M / FP8 | 4–14 tok/s |

> **Bandwidth Rule:** Memory bandwidth (GB/s), not raw TFLOPS, is the primary performance bottleneck for local LLM token generation. Apple Silicon's unified memory (ranging from 150 GB/s on base chips to over 800 GB/s on Ultra chips) and high-end dedicated GDDR6X/HBM setups yield significantly higher tokens per second during the decoding phase.

---

## OS-Specific Installation & Driver Optimization

Ollama orchestrates compute offloading through specialized hardware runtimes: Metal on macOS, CUDA on Linux and Windows, and ROCm on supported AMD platforms.

### 1. macOS Deployment (Apple Silicon Optimized)
macOS manages VRAM dynamically through Unified Memory Architecture (UMA). By default, macOS reserves a percentage of memory for the operating system, which can cause out-of-memory errors on larger models like the 32B or 70B variants.

bash
# 1. Install Ollama via Homebrew
brew install ollama

# 2. Configure macOS to allocate up to 85% of unified memory to the GPU runtime
# Run via Terminal and restart your machine to apply the sysctl parameter
sudo sysctl iogpu.wired_mem_limit=34359738368  # Example: 32 GB in bytes

# 3. Launch the Ollama daemon as a persistent service
ollama serve
### 2. Linux Deployment (Ubuntu/Debian Enterprise Stack)
For Linux nodes running NVIDIA GPUs, verify your NVIDIA driver (>= 535.xx) and the NVIDIA Container Toolkit or direct CUDA runtime before starting Ollama.

bash
# 1. Fetch and execute the official Ollama deployment script
curl -fsSL https://ollama.com/install.sh | sh

# 2. Configure systemd overrides for multi-GPU setups or remote API binding
sudo systemctl edit ollama.service
Add the following environment variables to the systemd configuration file to expose the server across private subnets and configure concurrency:

ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_ORIGINS=*"
Environment="OLLAMA_NUM_PARALLEL=4"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="CUDA_VISIBLE_DEVICES=0,1"
Apply the changes and reload the service:

bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
sudo systemctl status ollama
### 3. Windows Deployment (Direct & WSL2 Configurations)
Windows users have two execution paths: the native Windows Ollama binary or an isolated WSL2 (Windows Subsystem for Linux) instance. Native execution is recommended for low-latency Direct3D/CUDA interop.

1. Download and run the official installer executable: `OllamaSetup.exe`.
2. Confirm CUDA access using PowerShell:
powershell
# Verify GPU availability inside PowerShell
nvidia-smi

# Set system-wide environment variables for the current session
$env:OLLAMA_NUM_PARALLEL = "2"
$env:OLLAMA_FLASH_ATTENTION = "1"

# Launch the Ollama executable manually if running detached
ollama serve
---

## Model Selection, Initialization, and Modelfile Customization

Ollama hosts DeepSeek-R1 distilled variants directly through its public registry under the `deepseek-r1` namespace, alongside quantized checkpoints of the full 671B model.

### 1. Pulling and Running Common Variants

bash
# Ultra-lightweight reasoning (Ideal for low-spec edge compute / 8GB machines)
ollama run deepseek-r1:1.5b

# Balanced reasoning for 8GB-12GB VRAM GPUs (RTX 3060/4060, M1/M2/M3)
ollama run deepseek-r1:7b

# High-precision mathematical and coding engine (Requires 24GB VRAM)
ollama run deepseek-r1:32b

# Enterprise-tier reasoning (Requires 48GB+ VRAM or Unified Memory)
ollama run deepseek-r1:70b
### 2. Building a Custom Enterprise Modelfile
To maximize throughput and enforce strict context-window limits, build an encapsulated `Modelfile`. This allows you to tune context depth (`num_ctx`), temperature, and internal system prompts.

Create a file named `Modelfile.deepseek-custom`:

dockerfile
FROM deepseek-r1:14b

# Set KV Cache context length (Default: 2048, Expanded: 32768)
PARAMETER num_ctx 32768

# Context processing temperature
# Lower values (0.5 - 0.7) are recommended for DeepSeek-R1 reasoning
PARAMETER temperature 0.6

# Set repeat penalty to mitigate redundant reasoning loops
PARAMETER repeat_penalty 1.15

# Allocate full layer offloading to available GPUs
PARAMETER num_gpu 99

# System instructions to configure deterministic reasoning
SYSTEM """
You are a Principal Software Architect and Systems Researcher.
When resolving complex problems:
1. Conduct complete architectural evaluations inside the <think> reasoning envelope.
2. Provide verified, edge-case-tested code snippets following the thought traces.
3. Keep final explanations concise, actionable, and mathematically grounded.
"""
Compile and register the model with the local daemon:

bash
ollama create deepseek-r1-architect -f ./Modelfile.deepseek-custom
ollama run deepseek-r1-architect
---

## Production Integration via Python SDK

Ollama provides a local REST API compliant with OpenAI-style endpoints (`http://localhost:11434/v1`). You can integrate it into internal production services using the native `ollama-python` client.

DeepSeek-R1 outputs explicit `<think>...</think>` tags containing its chain-of-thought traces. The following production-ready Python script handles streaming responses, separates internal reasoning from customer-facing text, and enforces fault tolerance.

python
#!/usr/bin/env python3
"""
DeepSeek-R1 Stream Processor with Ollama
Separates real-time reasoning traces from final inference outputs.
"""

import sys
import re
from typing import Generator
import ollama

def stream_deepseek_reasoning(
    prompt: str, 
    model: str = "deepseek-r1:14b"
) -> Generator[tuple[str, str], None, None]:
    """
    Streams output from DeepSeek-R1 via Ollama.
    Yields tuples of (channel_type, token_chunk) where:
    - channel_type is either 'THOUGHT' or 'RESPONSE'
    """
    client = ollama.Client(host='http://127.0.0.1:11434')
    
    messages = [{"role": "user", "content": prompt}]
    
    stream = client.chat(
        model=model,
        messages=messages,
        stream=True,
        options={
            "temperature": 0.6,
            "num_ctx": 16384,
            "top_p": 0.95
        }
    )
    
    in_thought_block = False
    
    for chunk in stream:
        content = chunk['message']['content']
        if not content:
            continue
            
        if "<think>" in content:
            in_thought_block = True
            content = content.replace("<think>", "")
            
        if "</think>" in content:
            parts = content.split("</think>")
            thought_part = parts[0]
            response_part = parts[1] if len(parts) > 1 else ""
            
            if thought_part:
                yield ("THOUGHT", thought_part)
            in_thought_block = False
            
            if response_part:
                yield ("RESPONSE", response_part)
            continue
            
        if in_thought_block:
            yield ("THOUGHT", content)
        else:
            yield ("RESPONSE", content)

if __name__ == "__main__":
    test_query = (
        "Design a distributed rate-limiting algorithm using Redis and token buckets. "
        "Detail the Lua script implementation to prevent race conditions."
    )
    
    print(f"[Connecting to Ollama...] Processing prompt:\n'{test_query}'\n")
    print("=" * 60)
    print("CHAIN OF THOUGHT TRACES:")
    print("=" * 60)
    
    current_channel = "THOUGHT"
    
    for channel, token in stream_deepseek_reasoning(test_query, model="deepseek-r1:14b"):
        if channel != current_channel and channel == "RESPONSE":
            print("\n\n" + "=" * 60)
            print("FINAL ARCHITECTURAL SPECIFICATION:")
            print("=" * 60)
            current_channel = "RESPONSE"
            
        sys.stdout.write(token)
        sys.stdout.flush()
    print("\n")
---

## Enterprise Developer Tip

> **Pro-Tip for Distributed Infrastructure Teams:**
> Running full-scale DeepSeek-V3 or uncompressed 671B R1 models locally requires significant VRAM (often 400GB+). If your local workstations can't support models beyond the 32B or 70B distilled versions, consider running hybrid deployments.
>
> You can claim **$200 to $300 in free compute credits** across cloud platforms like **Lambda Labs, RunPod, or DigitalOcean GPU Droplets**. This gives you on-demand access to multi-GPU nodes (such as 8x A100/H100 rigs) running Ollama inside an ephemeral Docker container. You can then route your lower-overhead workloads through your local Ollama instance and offload full-precision 671B inference to your remote clusters using the exact same API client.

---

## Performance Optimization & Troubleshooting

When scaling up local models, inference speed can drop significantly if the runtime is misconfigured. Common bottlenecks include out-of-memory errors, low tokens-per-second, and unstable execution loops.

┌────────────────────────────────────────┐
          │      Inference Bottleneck Triage       │
          └───────────────────┬────────────────────┘
                              │
             Is RAM/VRAM usage exceeding capacity?
                     ┌────────┴────────┐
                    YES                NO
                     │                 │
           Reduce `num_ctx`      Are tokens/sec low?
           or move to a higher         │
           quantization level   ┌──────┴──────┐
           (e.g., 32B to 14B)  YES            NO
                                │             │
                    Check layer offload   System healthy
                    (`num_gpu 99`) &
                    enable Flash Attention
### 1. Context Window Memory Explosion
The memory footprint of the Key-Value (KV) cache grows linearly with context size:

$$\text{KV Cache Memory} \approx 2 \times \text{Layers} \times \text{Heads} \times \text{Head Dimension} \times \text{Context Length} \times \text{Precision (Bytes)}$$

While MLA dramatically compresses this calculation, configuring a 64k or 128k context on unified memory systems can still consume tens of gigabytes of RAM. If Ollama crashes unexpectedly (`CUDA out of memory` or `SIGKILL`), reduce your `num_ctx` in the `Modelfile` to `8192` or `16384` before scaling back up.

### 2. Ensuring Complete GPU Layer Offloading
When working with mid-sized models like `deepseek-r1:32b`, Ollama may offload only a portion of the layers to your GPU, processing the remaining layers on the CPU. This creates an immediate memory bandwidth bottleneck across the PCIe bus.

Run `ollama ps` while running a prompt to inspect layer allocation:

bash
ollama ps
# Look for the PROCESSOR column:
# Ideal state:   "100% GPU"
# Warning state: "65%/35% CPU/GPU" -> Severe latency degradation
To resolve partial offloading:
* Increase system shared memory limits.
* Close external processes consuming VRAM.
* Drop from a higher-precision quantization down to an optimized variant (e.g., from `Q8_0` to `Q4_K_M`).

### 3. Flash Attention & Concurrency Flags
On modern NVIDIA GPUs (Ampere architectures and newer: RTX 30xx/40xx, A100, H100), explicitly enable Flash Attention. This significantly reduces the memory footprint of intermediate attention steps and boosts inference speeds:

bash
# Add to your execution profile or terminal startup file
export OLLAMA_FLASH_ATTENTION=1
export OLLAMA_KV_CACHE_TYPE="f16" # Switch to "q8_0" or "q4_0" on low-VRAM GPUs
---

## Frequently Asked Questions

### What is the practical difference between DeepSeek-V3 and DeepSeek-R1?
DeepSeek-V3 is an ultra-fast base/chat model designed for high-throughput language generation, complex coding, and structured output. DeepSeek-R1 is a reasoning-specialized model that uses dynamic internal Chain-of-Thought (CoT) traces (`<think>` loops) to plan, verify, and correct its logic before generating a response. Use V3 for direct chat, summarization, and standard software engineering; use R1 for logic puzzles, deep mathematical derivation, system architecture design, and complex algorithmic debugging.

### Can I run the full 671B DeepSeek-R1 locally with Ollama?
Yes, provided your hardware meets the memory bandwidth and capacity requirements. A quantized 4-bit (Q4_K_M) build of the 671B model requires approximately 400 GB of addressable memory. You can run it on a dual-CPU workstation with 512 GB of high-speed DDR5 ECC RAM (though generation speeds will be slow, around 2–4 tokens per second), on high-end Apple Silicon hardware (like an M2/M3/M4 Ultra with 128 GB–192 GB running aggressive 1.58-bit/2-bit quantizations), or across enterprise multi-GPU clusters (such as 8x A100/H100 systems). For everyday local development, the distilled variants (`14b` and `32b`) offer the best balance of speed and reasoning quality.

### Why are the distilled models based on Qwen and Llama instead of DeepSeek's MoE architecture?
Training fine-grained Mixture-of-Experts architectures at lower parameter counts (such as 1.5B to 14B) reduces parameter density per expert, which often hurts token generation quality. To deliver high-performance models for consumer hardware, the DeepSeek team distilled hundreds of thousands of R1 reasoning trajectories directly into proven dense architectures—specifically Qwen 2.5 and Llama 3.3. This approach preserves R1's step-by-step reasoning style while keeping hardware requirements accessible.

### How do I hide or parse DeepSeek-R1's `<think>` tags in web applications?
DeepSeek-R1 structures its chain-of-thought logic between `<think>` and `</think>` XML delimiters. In client applications or API pipelines, you can capture these sections using regular expressions or streaming state machines (as shown in the Python implementation above). This allows you to display reasoning traces in expandable UI accordions for visibility while sending only the final response back to your core user flows or downstream systems.

### Does Ollama support continuous multi-GPU tensor parallelism for DeepSeek?
Yes. Ollama automatically detects and pools multiple identical NVIDIA GPUs via CUDA. It distributes model layers across available devices based on available memory and compute capacity. For advanced multi-node configurations, Ollama relies on its underlying `llama.cpp` runtime, which can be compiled directly with MPI or RPC backends to distribute workloads across discrete compute nodes on your network.