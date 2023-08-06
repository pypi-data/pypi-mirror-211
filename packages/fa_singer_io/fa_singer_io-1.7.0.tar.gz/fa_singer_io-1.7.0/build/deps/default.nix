{
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    inherit (nixpkgs."${python_version}".pkgs) buildPythonPackage;
    inherit (nixpkgs.python3Packages) fetchPypi;
  };

  utils = import ./override_utils.nix;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;

  layer_1 = python_pkgs:
    python_pkgs
    // {
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      purity = nixpkgs.purity."${python_version}".pkg;
      types-jsonschema = import ./jsonschema/stubs.nix lib;
      types-pyRFC3339 = import ./pyRFC3339/stubs.nix lib;
    };

  pyrsistent_override = python_pkgs:
    utils.replace_pkg ["pyrsistent"] (
      python_pkgs.pyrsistent.overridePythonAttrs (
        _: {doCheck = false;}
      )
    );
  networkx_override = python_pkgs: utils.replace_pkg ["networkx"] (import ./networkx.nix lib python_pkgs);
  overrides = map pkgs_overrides [
    pyrsistent_override
    networkx_override
  ];

  python_pkgs = utils.compose ([layer_1] ++ overrides) nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
}
