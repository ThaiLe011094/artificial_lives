{ pkgs ? import <nixpkgs> { config.allowUnfree = true; } }:

let
  libPath = with pkgs; lib.makeLibraryPath [
    stdenv.cc.cc.lib
    zlib
    glib
    xorg.libX11
    libglvnd
    cudaPackages.cudatoolkit
    cudaPackages.cudnn
    postgresql.pg_config
    postgresql
    openssl
  ];
in
pkgs.mkShell {
  name = "tensorflow-venv-env";

  buildInputs = with pkgs; [
    python3
    cudaPackages.cudatoolkit
    cudaPackages.cudnn
    git
    stdenv.cc.cc.lib
    pkgs.postgresql
    pkgs.openssl
    gcc
    python312Packages.setuptools
  ];

  shellHook = ''
    # 1. Automatically activate venv in <project_root>/.venv
    if [ -f "../self_experiments/.venv/bin/activate" ]; then
      source ../self_experiments/.venv/bin/activate
      echo "Activated virtualenv from .venv"
    else
      echo "Warning: venv not found at .venv"
    fi

    # 2. Fix missing libraries
    export LD_LIBRARY_PATH="${libPath}:/run/opengl-driver/lib:$LD_LIBRARY_PATH"
    export LD_LIBRARY_PATH="${pkgs.postgresql.lib}/lib:$LD_LIBRARY_PATH"

    # 3. Force to use dedicated GPU (PRIME Offload)
    export __NV_PRIME_RENDER_OFFLOAD=1
    export __GLX_VENDOR_LIBRARY_NAME=nvidia

    # 4. Fix TensorFlow could not find CUDA in venv
    export CUDA_PATH=${pkgs.cudaPackages.cudatoolkit}
    export EXTRA_LDFLAGS="-L/lib -L${pkgs.linuxPackages.nvidia_x11}/lib"
    export EXTRA_CCFLAGS="-I/usr/include"

    # 5. Fix missing pg_config
    export PATH="${pkgs.postgresql.pg_config}/bin:${pkgs.postgresql}/bin:$PATH"
    export C_INCLUDE_PATH="${pkgs.postgresql.dev}/include:${pkgs.openssl.dev}/include:$C_INCLUDE_PATH"
    export LIBRARY_PATH="${pkgs.postgresql.lib}/lib:${pkgs.openssl.out}/lib:$LIBRARY_PATH"
    export PGPATH="${pkgs.postgresql.pg_config}/bin/pg_config"

    # 6. Fix C++ build issues
    export CPATH="${pkgs.stdenv.cc.cc}/include/c++/${pkgs.gcc.version}:${pkgs.stdenv.cc.cc}/include/c++/${pkgs.gcc.version}/x86_64-unknown-linux-gnu:$CPATH"
    export LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:$LIBRARY_PATH"
    export SETUPTOOLS_USE_DISTUTILS=local
  '';
}
