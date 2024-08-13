import { Stack, aws_dynamodb as ddb } from 'aws-cdk-lib'
import type { App, StackProps } from 'aws-cdk-lib'

export class PersistenceStack extends Stack {
  constructor(scope: App, id: string, props: StackProps) {
    super(scope, id, props)

    // Create DDB table for LD Relay Proxy
    const relayProxyTable = new ddb.Table(this, `openpowerlifting-graphs-table`, {
      tableName: `openpowerlifting-graphs`,
      partitionKey: {
        name: 'Name',
        type: ddb.AttributeType.STRING,
      },
      sortKey: {
        name: 'Date',
        type: ddb.AttributeType.STRING,
      },
      billingMode: ddb.BillingMode.PAY_PER_REQUEST,
    })
  }
}
