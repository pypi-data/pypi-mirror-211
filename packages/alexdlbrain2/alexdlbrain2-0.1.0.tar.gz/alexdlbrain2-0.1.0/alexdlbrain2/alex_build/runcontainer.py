import subprocess


def run_singularity_container():
    # 创建或更新 Singularity 容器
    build_cmd = [
        "sudo",
        "singularity",
        "build",
        "alex_build_v01.sif",
        "alex_build_v01.def",
    ]
    subprocess.run(build_cmd, check=True)

    slurm_cmd = [
        "srun",
        "-p",
        "qTRDGPUL",
        "-v",
        "-n1",
        "-c",
        "64",
        "--gres=gpu:a100:4",
        "--mem=500G",
        "--pty",
        "/bin/bash",
    ]
    # Run Interactive SLURM job with A100
    subprocess.run(slurm_cmd, check=True)

    # 运行 Singularity 容器并执行 Python 脚本
    run_cmd = [
        "singularity",
        "shell",
        "--nv",
        "--bind",
        "./:/code",
        "--bind",
        "/data/users2/afedorov/data/imagenet_blurred/:/datasets/",
        "/data/users2/afedorov/singularity/alex_build_v01.sif",
    ]
    subprocess.run(run_cmd, check=True)
