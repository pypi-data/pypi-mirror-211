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
      import-linter = import ./import-linter.nix lib python_pkgs;
      more-itertools = import ./more-itertools.nix lib python_pkgs;
      types-deprecated = import ./deprecated/stubs.nix lib;
      types-simplejson = import ./simplejson/stubs.nix lib;
    };

  networkx_override = python_pkgs: utils.replace_pkg ["networkx"] (import ./networkx.nix lib python_pkgs);
  overrides = map pkgs_overrides [
    networkx_override
  ];

  python_pkgs = utils.compose ([layer_1] ++ overrides) nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
}
