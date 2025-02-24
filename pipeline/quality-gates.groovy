def check() {
    def coverage = sh(script: 'coverage report', returnStdout: true).trim()
    def minCoverage = 80
    
    def pylintScore = sh(script: 'pylint --score app/', returnStdout: true).trim()
    def minPylintScore = 8
    
    if (coverage < minCoverage || pylintScore < minPylintScore) {
        return false
    }
    return true
}
return this