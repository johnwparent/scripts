@echo OFF

git reset --soft HEAD~1
git restore --staged lib/spack/llnl/util/filesystem.py
git commit --reuse-message ORIG_HEAD

set msg="Hello World"

SETLOCAL ENABLEDELAYEDEXPANSION
SET count=1
FOR /F "tokens=* USEBACKQ" %%F IN (`"git show -s --format=%%B ORIG_HEAD"`) DO (
  if !count!==1 SET msg=%%F
  SET /a count=!count!+1
)
git stage lib/spack/llnl/util/filesystem.py
git commit -m"%msg% - filesystem"

ENDLOCAL
