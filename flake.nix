{
  description = "Aufré-dit Streamlit App Dev Shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    supportedSystems = [
      "x86_64-linux"
      "aarch64-linux"
      "x86_64-darwin"
      "aarch64-darwin"
    ];
    forEachSupportedSystem = f:
      nixpkgs.lib.genAttrs supportedSystems (system:
        f {
          pkgs = import nixpkgs {inherit system;};
        });
  in {
    devShells = forEachSupportedSystem ({pkgs}: {
      default = let
        pythonEnv = pkgs.python3.withPackages (ps:
          with ps; [
            streamlit
            google-genai
            requests
            pytest
          ]);
      in
        pkgs.mkShell {
          name = "aufre-dit-devshell";

          buildInputs = with pkgs; [
            pythonEnv
            just
            git
            ruff
            pyright
            pre-commit
            ty
          ];

          shellHook = ''
            export LD_LIBRARY_PATH="${pkgs.stdenv.cc.cc.lib}/lib:${pkgs.zlib}/lib:${pkgs.glib.out}/lib:$LD_LIBRARY_PATH"

            echo "========================================================"
            echo "⚜️  Welcome to the Aufré-dit Streamlit Flake Dev Shell ⚜️"
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
        };
    });
  };
}
