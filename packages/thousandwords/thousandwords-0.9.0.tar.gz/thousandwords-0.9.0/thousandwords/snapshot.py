from IPython.core.magic import cell_magic, magics_class
from IPython import get_ipython
from thousandwords.share import ShareMagic

@magics_class
class SnapshotMagic(ShareMagic):
  """ Alias for %%share """

  @cell_magic("snapshot")
  def cmagic(self, line="", cell=""):
    super().cmagic(line, cell)

get_ipython().register_magics(SnapshotMagic)
