def approve() {
    def approvers = ['tech-lead', 'devops-lead']
    def approved = false
    
    timeout(time: 24, unit: 'HOURS') {
        approved = input(
            message: 'Deploy to production?',
            ok: 'Deploy',
            submitterParameter: 'APPROVER'
        )
    }
    
    if (!approvers.contains(approved.APPROVER)) {
        error "Unauthorized approver"
    }
    return true
}
return this