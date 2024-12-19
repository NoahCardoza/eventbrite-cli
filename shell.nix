{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.uv
  ];

  shellHook = ''
      # Create virtual environment if it doesn't exist
      if [ ! -d ".venv" ]; then
          uv sync
      fi
      source .venv/bin/activate
  '';
}