#!/usr/bin/env node
import { App } from 'aws-cdk-lib'
import { PersistenceStack } from './stacks/persistence'

const app = new App()

new PersistenceStack(app, 'LDRelayProxyECRRepoStack', {
  stackName: 'LDRelayECR',
  tags: {
    service: 'ld-relay-proxy',
  },
})


app.synth()
