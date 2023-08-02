from nbgrader.server_extensions.formgrader.handlers import (
    template_path as nbgrader_template_path,
)

from e2xgrader.server_extensions.apps.formgrader.handlers import (
    template_path as e2x_template_path,
)

from ..exporters import E2xExporter

preprocessors = dict(
    AssignLatePenalties="nbgrader.preprocessors.AssignLatePenalties",
    CSSPreprocessor="nbconvert.preprocessors.CSSHTMLHeaderPreprocessor",
    CheckCellMetadata="nbgrader.preprocessors.CheckCellMetadata",
    ClearHiddenTests="e2xgrader.preprocessors.ClearHiddenTests",
    ClearMarkScheme="nbgrader.preprocessors.ClearMarkScheme",
    ClearOutput="nbgrader.preprocessors.ClearOutput",
    ClearSolutions="e2xgrader.preprocessors.ClearSolutions",
    ComputeChecksums="nbgrader.preprocessors.ComputeChecksums",
    DeduplicateIds="nbgrader.preprocessors.DeduplicateIds",
    Execute="nbgrader.preprocessors.Execute",
    ExtractAttachments="e2xgrader.preprocessors.ExtractAttachments",
    FilterTests="e2xgrader.preprocessors.FilterTests",
    GetGrades="nbgrader.preprocessors.GetGrades",
    IncludeHeaderFooter="nbgrader.preprocessors.IncludeHeaderFooter",
    LimitOutput="nbgrader.preprocessors.LimitOutput",
    LockCells="nbgrader.preprocessors.LockCells",
    OverwriteCells="e2xgrader.preprocessors.OverwriteCells",
    OverwriteKernelspec="nbgrader.preprocessors.OverwriteKernelspec",
    SaveAutoGrades="e2xgrader.preprocessors.SaveAutoGrades",
    SaveCells="e2xgrader.preprocessors.SaveCells",
    UnpermuteTasks="e2xgrader.preprocessors.UnpermuteTasks",
    Unscramble="e2xgrader.preprocessors.Unscramble",
    ValidateExtracCells="e2xgrader.preprocessors.ValidateExtraCells",
)


def configure_feedback(config):
    config.GenerateFeedback.preprocessors = [
        preprocessors["GetGrades"],
        preprocessors["FilterTests"],
        preprocessors["CSSPreprocessor"],
    ]
    config.GenerateFeedback.exporter_class = E2xExporter
    config.HTMLExporter.extra_template_basedirs = [
        e2x_template_path,
        nbgrader_template_path,
    ]


def configure_base(config):
    config.Autograde.sanitize_preprocessors = [
        preprocessors["ClearOutput"],
        preprocessors["DeduplicateIds"],
        preprocessors["OverwriteKernelspec"],
        preprocessors["OverwriteCells"],
        preprocessors["CheckCellMetadata"],
        preprocessors["UnpermuteTasks"],
        preprocessors["Unscramble"],
    ]
    config.Autograde.autograde_preprocessors = [
        preprocessors["ExtractAttachments"],
        preprocessors["Execute"],
        preprocessors["LimitOutput"],
        preprocessors["SaveAutoGrades"],
        preprocessors["AssignLatePenalties"],
        preprocessors["CheckCellMetadata"],
    ]
    config.GenerateAssignment.preprocessors = [
        preprocessors["ValidateExtracCells"],
        preprocessors["IncludeHeaderFooter"],
        preprocessors["LockCells"],
        preprocessors["ClearSolutions"],
        preprocessors["ClearOutput"],
        preprocessors["CheckCellMetadata"],
        preprocessors["ComputeChecksums"],
        preprocessors["SaveCells"],
        preprocessors["ClearHiddenTests"],
        preprocessors["ClearMarkScheme"],
        preprocessors["ComputeChecksums"],
        preprocessors["CheckCellMetadata"],
    ]
    configure_feedback(config)


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
