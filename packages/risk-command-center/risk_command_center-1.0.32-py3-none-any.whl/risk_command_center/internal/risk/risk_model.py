#
# riskId: String,
# departmentId: String,
# riskTypeId: String,
# userId: String,
# userName: String,
# riskName: String,
# riskSource: String,
# riskEffect: String,
# riskTrigger: String,
# riskCrossArea: Bool,
# orgId: String,
# riskDate: Date

class RiskModel:
    def __init__(self, riskId, departmentId, riskTypeId, userId, userName, riskName, riskSource, riskEffect, riskTrigger, riskCrossArea, orgId, riskDate):
        self.riskId = riskId
        self.departmentId = departmentId
        self.riskTypeId = riskTypeId
        self.userId = userId
        self.userName = userName
        self.riskName = riskName
        self.riskSource = riskSource
        self.riskEffect = riskEffect 
        self.riskTrigger = riskTrigger
        self.riskCrossArea = riskCrossArea
        self.orgId = orgId
        self.riskDate = riskDate