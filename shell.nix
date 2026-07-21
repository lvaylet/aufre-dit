{pkgs ? import <nixpkgs> {}}: let
  # Build python environment containing the required dependencies from nixpkgs
  pythonEnv = pkgs.python3.withPackages (ps:
    with ps; [
      streamlit
      google-genai
      httpx
      pydantic
      pydantic-settings
      pytest
    ]);
in
  pkgs.mkShell {
    name = "aufre-dit-devshell";

    buildInputs = with pkgs; [
      pythonEnv
      uv
      just
      git
      ruff
      pyright
      pre-commit
      ty
    ];

    shellHook = ''
      # Expose CC compiler and standard libraries for potential pip compiling inside shell
      export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:${pkgs.glib.out}/lib:$LD_LIBRARY_PATH"

      echo "========================================================"
      echo "⚜️  Welcome to the Aufré-dit Streamlit Dev Shell (NixOS) ⚜️"
      echo "========================================================"
      echo "Available tools in this environment:"
      echo "  - python3  : ${pkgs.python3.version}"
      echo "  - streamlit: ${pkgs.python3Packages.streamlit.version}"
      echo "  - just     : ${pkgs.just.version}"
      echo "  - ruff     : ${pkgs.ruff.version}"
      echo "  - pyright  : ${pkgs.pyright.version}"
      echo "  - ty       : ${pkgs.ty.version}"
      echo "========================================================"
      echo "Tips:"
      echo "  * To run the app directly: streamlit run app.py"
      echo "  * To run via just (bypassing venv): just --set bin_dir \"\" run"
      echo "  * Or to initialize a venv inheriting Nix packages:"
      echo "    python3 -m venv --system-site-packages .venv"
      echo "========================================================"
    '';
  }
