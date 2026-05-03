"""Allows ``python -m markast`` to invoke the CLI."""
from markast.cli import main
import sys

sys.exit(main())
