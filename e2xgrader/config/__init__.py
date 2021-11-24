from ..exporters import E2xExporter


def configure_base(config):
    config.Autograde.sanitize_preprocessors = [
        "nbgrader.preprocessors.ClearOutput",
        "nbgrader.preprocessors.DeduplicateIds",
        "nbgrader.preprocessors.OverwriteKernelspec",
        "e2xgrader.preprocessors.OverwriteCells",
        "nbgrader.preprocessors.CheckCellMetadata",
        "e2xgrader.preprocessors.UnpermuteTasks",
        "e2xgrader.preprocessors.Unscramble",
    ]
    config.Autograde.autograde_preprocessors = [
        "e2xgrader.preprocessors.ExtractAttachments",
        "nbgrader.preprocessors.Execute",
        "nbgrader.preprocessors.LimitOutput",
        "e2xgrader.preprocessors.SaveAutoGrades",
        "nbgrader.preprocessors.AssignLatePenalties",
        "nbgrader.preprocessors.CheckCellMetadata",
    ]
    config.GenerateAssignment.preprocessors = [
        "e2xgrader.preprocessors.ValidateExtraCells",
        "nbgrader.preprocessors.IncludeHeaderFooter",
        "nbgrader.preprocessors.LockCells",
        "e2xgrader.preprocessors.ClearSolutions",
        "nbgrader.preprocessors.ClearOutput",
        "nbgrader.preprocessors.CheckCellMetadata",
        "nbgrader.preprocessors.ComputeChecksums",
        "e2xgrader.preprocessors.SaveCells",
        "e2xgrader.preprocessors.ClearHiddenTests",
        "nbgrader.preprocessors.ClearMarkScheme",
        "nbgrader.preprocessors.ComputeChecksums",
        "nbgrader.preprocessors.CheckCellMetadata",
    ]
    config.GenerateFeedback.preprocessors = [
        "nbgrader.preprocessors.GetGrades",
        "e2xgrader.preprocessors.FilterTests",
        "nbconvert.preprocessors.CSSHTMLHeaderPreprocessor",
    ]
    config.GenerateFeedback.exporter_class = E2xExporter


def configure_exchange(config):
    config.ExchangeFactory.exchange = "e2xgrader.exchange.E2xExchange"
    config.ExchangeFactory.submit = "e2xgrader.exchange.E2xExchangeSubmit"
    config.ExchangeFactory.collect = "e2xgrader.exchange.E2xExchangeCollect"
    config.ExchangeFactory.fetch_assignment = (
        "e2xgrader.exchange.E2xExchangeFetchAssignment"
    )
    config.ExchangeFactory.release_assignment = (
        "e2xgrader.exchange.E2xExchangeReleaseAssignment"
    )
    config.ExchangeFactory.list = "e2xgrader.exchange.E2xExchangeList"
    config.ExchangeFactory.fetch_feedback = (
        "e2xgrader.exchange.E2xExchangeFetchFeedback"
    )
    config.ExchangeFactory.release_feedback = (
        "e2xgrader.exchange.E2xExchangeReleaseFeedback"
    )
