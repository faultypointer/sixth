{
  description =
    "An empty flake template that you can adapt to your own environment";

  # Flake inputs
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  # Flake outputs
  outputs = { self, nixpkgs }:
    let
      # The systems supported for this flake
      supportedSystems = [
        "x86_64-linux" # 64-bit Intel/AMD Linux
        "aarch64-linux" # 64-bit ARM Linux
        "x86_64-darwin" # 64-bit Intel macOS
        "aarch64-darwin" # 64-bit ARM macOS
      ];

      # Helper to provide system-specific attributes
      forEachSupportedSystem = f:
        nixpkgs.lib.genAttrs supportedSystems
        (system: f { pkgs = import nixpkgs { inherit system; }; });
    in {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          # The Nix packages provided in the environment
          # Add any you need here
          packages = with pkgs;
            [ python312 jupyter-all ] ++ (with pkgs.python312Packages; [
              ipython
              numpy
              tkinter
              customtkinter
              networkx
              scikit-learn
              scipy
              pandas
              matplotlib
              seaborn
              ipykernel
              sympy
              torch
              torchvision
              torchinfo
              tqdm
              nltk
              wordcloud
              xgboost
              umlet
            ]);
        };
      });
    };
}
