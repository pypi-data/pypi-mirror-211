import setuptools
import glob

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="gwsci-pastro",
  version="1.0.0",
  author="Chad Hanna, Victoria Niu, Leo Tsukada, Anarya Ray",
  author_email="chad.hanna@ligo.org",
  description="Tools for calculating astrophysical probability of GW events",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://git.ligo.org/gstlal/pastro",
  packages=["pastro",],
  classifiers=[
   	"Programming Language :: Python :: 3",
   	'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        "Operating System :: OS Independent",
  ],
  scripts = glob.glob("bin/*"),
  python_requires='>=3.6',
)
