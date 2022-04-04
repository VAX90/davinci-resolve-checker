local_str = {
    "locale": "Usando localidade:",
    "project name": "Verificador DaVinci Resolve",
    "you are running": "Você está rodando",
    "script not tested on distro": "mas este script não foi testado nele.",
    "which DR package": "Pacote DaVinci Resolve instalado:",
    "openCL drivers": "Drivers OpenCL instalados:",
    "presented gpus": "GPUs apresentadas:",
    "kernel driver": "Driver do Kernel em uso:",
    "opengl vendor": "String do fornecedor OpenGL:",
    "missing opengl vendor": "Não foi possível detectar string do fornecedor OpenGL. Provavelmente você está tentando usar AMD Pro OpenGL enquanto sua GPU principal é Intel. Além disso, provavelmente você está executando este script via ssh.",
    "should uninstall opencl-mesa": "Você precisa desinstalar o opencl-mesa. Do contrário, Davinci Resolve (v17.1.1) se comporta com erro: imagem está corrompida. Mas se você desmarcar a caixa de seleção em configurações e reiniciar o Davinci Resolve, então toda a sua sessão desktop pode ficar corrompida e somente reiniciando a máquina irá resolver. Este comportamento é observado ao menos em GPU AMD.",
    "several intel gpus": "Você tem várias GPUs Intel. Estou confuso. Você está usando uma placa-mãe com múltiplas CPUs? Ou iGPU Intel + dGPU Intel (o que não existia até o momento que isto foi escrito)?",
    "several amd gpus": "Você tem várias GPUs AMD. Estou confuso, qual delas pretende usar?",
    "several nvidia gpus": "Você tem várias GPUs NVIDIA. Estou confuso, qual delas pretende usar?",
    "confused by nvidia and amd gpus": "Você tem GPUs da AMD e NVIDIA. Estou confuso, qual delas pretende usar?",
    "amd gpu binded to vfio-pci": "Sua GPU AMD está vinculada a vfio-pci, interrompendo as verificações.",
    "nvidia gpu binded to vfio-pci": "Sua GPU NVIDIA está vinculada a  vfio-pci, interrompendo as verificações.",
    "only intel gpu, cannot run DR": "Você só possui GPU Intel. Neste momento, Davinci Resolve não pode usar GPUs Intel para OpenCL. Você não pode rodar o Davinci Resolve. Veja (em inglês): https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=81579",
    "switch from radeon driver to amdgpu": "Você está usando driver RADEON. Mude para amdgpu como descrito aqui (em inglês): https://wiki.archlinux.org/title/AMDGPU#Enable_Southern_Islands_(SI)_and_Sea_Islands_(CIK)_support. Caso contrário, não poderá rodar o Davinci Resolve",
    "no support for amd driver, cannot run DR": "Sua GPU só suporta driver RADEON. O DaVinci Resolve requer amdgpu progl, que só funciona com amdgpu driver. Você não pode rodar o DaVinci Resolve.",
    "not running amdgpu driver, cannot run DR": "Você está rodando amdgpu driver e não pode rodar o DaVinci Resolve.",
    "missing opencl driver": "Você não tem opencl-driver para AMD GPU. Instale-o, caso contrário não poderá usar o DaVinci Resolve.",
    "good to run DR": "Tudo em ordem. Você deve conseguir usar o DaVinci Resolve com sucesso!",
    "missing opencl-nvidia package": "Você não tem o pacote opencl-nvidia (ou pacote alternativo que ofereça opencl-nvidia). Instale-o, caso contrário não poderá usar o DaVinci Resolve. Ainda que planeje usar cuda, opencl-nvidia é uma dependência necessária.",
    "missing nvidia as kernel driver": "Você não está usando nvidia como driver do kernel. Use um driver nvidia proprietário, caso contrário não poderá usar o DaVinci Resolve.",
    "not running nvidia rendered": "Você não está rodando o renderizador NVIDIA. Tente rodar o script com prime-run (vide README) ou outro método para optimus, caso contrário não poderá usar o DaVinci Resolve.",
}
