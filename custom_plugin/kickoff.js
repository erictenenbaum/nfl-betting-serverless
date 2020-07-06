'use strict';
class Kickoff {
    constructor(serverless) {
        this.serverless = serverless;
        this.provider = this.serverless.getProvider('aws');
        this.hooks = {
            'after:deploy:deploy': () => this.afterDeployFunction()
        };
    }
    afterDeployFunction() {
        this.provider.request('Lambda', 'invoke', {
            FunctionName: 'nfl-betting-serverless-dev-prep-data'
        });        
    }
}
module.exports = Kickoff;