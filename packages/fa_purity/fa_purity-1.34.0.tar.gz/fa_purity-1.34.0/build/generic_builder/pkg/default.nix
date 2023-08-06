{
  buildPythonPackage,
  metadata,
  pkg_deps,
  src,
}: let
  arch_check = ./check/arch.sh;
  type_check = ./check/types.sh;
  test_check = ./check/tests.sh;
in
  buildPythonPackage {
    inherit arch_check src type_check test_check;
    inherit (metadata) version;
    pname = metadata.name;
    format = "pyproject";
    checkPhase = [
      ''
        source ${type_check} \
        && source ${test_check} \
        && source ${arch_check}
      ''
    ];
    doCheck = true;
    pythonImportsCheck = [metadata.name];
    buildInputs = pkg_deps.build_deps;
    propagatedBuildInputs = pkg_deps.runtime_deps;
    checkInputs = pkg_deps.test_deps;
    nativeCheckInputs = pkg_deps.test_deps;
  }
