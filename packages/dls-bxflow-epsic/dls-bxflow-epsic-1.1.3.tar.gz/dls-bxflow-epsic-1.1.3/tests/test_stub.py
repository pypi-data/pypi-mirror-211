import logging

from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------
class TestStub(BaseTester):

    # ----------------------------------------------------------------------------------------
    def test(
        self,
        logging_setup: None,
        output_directory: str,
    ) -> None:
        """
        Run the test science outside of any bxflow workflow framework.

        Instantiates the txrm science class and runs it.

        Args:
            logging_setup (Any): logging setup created by the fixture
            output_directory (str): output directory assigned by the fixture.
                The output directory is typically in /tmp/dls-bxflow-epsic.
                It is wiped clean before the test, but left standing after the test.

        The output directory is set up as the current working directory
        before the science class is called.
        """

        self.main(output_directory)

    # ----------------------------------------------------------------------------------------
    async def _main_coroutine(
        self,
        output_directory: str,
    ) -> None:
        """
        Run the test inside an asyncio coroutine.
        """

        logger.debug("this is just a stub")
