c = get_config()

c.Autograde.sanitize_preprocessors = [
    "nbgrader.preprocessors.ClearOutput",
    "nbgrader.preprocessors.DeduplicateIds",
    "nbgrader.preprocessors.OverwriteKernelspec",
    "e2xgrader.preprocessors.OverwriteCells",
    "nbgrader.preprocessors.CheckCellMetadata",
    "e2xgrader.preprocessors.UnpermuteTasks",
    "e2xgrader.preprocessors.Unscramble",
]

c.Autograde.autograde_preprocessors = [
    "nbgrader.preprocessors.Execute",
    "nbgrader.preprocessors.LimitOutput",
    "e2xgrader.preprocessors.SaveAutoGrades",
    "nbgrader.preprocessors.AssignLatePenalties",
    "nbgrader.preprocessors.CheckCellMetadata",
]

c.GenerateAssignment.preprocessors = [
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

# Set up the exchange

# c.ExchangeFactory.exchange = 'e2xgrader.exchange.E2xExchange'
# c.ExchangeFactory.submit = 'e2xgrader.exchange.E2xExchangeSubmit'
# c.ExchangeFactory.collect = 'e2xgrader.exchange.E2xExchangeCollect'
# c.ExchangeFactory.fetch_assignment = 'e2xgrader.exchange.E2xExchangeFetchAssignment'
# c.ExchangeFactory.release_assignment = 'e2xgrader.exchange.E2xExchangeReleaseAssignment'
# c.ExchangeFactory.list = 'e2xgrader.exchange.E2xExchangeList'

# c.Exchange.personalized_inbound = True
# c.Exchange.personalized_outbound = True
