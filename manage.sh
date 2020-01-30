AVAILABLE_MODES="[clean|publish]"

echo "Enter mode: $AVAILABLE_MODES"
read mode

if [ $mode = "clean" ]
then
  echo "Cleaning cached files.."
  rm -rf build
  rm -rf dist
  rm -rf *.egg-info
  echo "Done."
elif [ $mode = "publish" ]
then
  echo "Publishing to PyPI.."
  python setup.py sdist bdist_wheel
  twine check dist/*
  twine upload dist/*
  echo "Done."
else
  echo "Invalid mode $mode. Expect one of $AVAILABLE_MODES"
fi
