-- CreateTable
CREATE TABLE "transactions" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "amount" DOUBLE PRECISION NOT NULL,
    "merchantType" TEXT NOT NULL,
    "location" TEXT NOT NULL,
    "transactionTime" TEXT NOT NULL,
    "paymentMethod" TEXT NOT NULL,
    "deviceType" TEXT NOT NULL,
    "isInternational" BOOLEAN NOT NULL DEFAULT false,
    "previousFailedAttempts" INTEGER NOT NULL DEFAULT 0,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "transactions_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "fraud_predictions" (
    "id" TEXT NOT NULL,
    "transactionId" TEXT NOT NULL,
    "prediction" INTEGER NOT NULL,
    "isFraud" BOOLEAN NOT NULL,
    "fraudProbability" DOUBLE PRECISION NOT NULL,
    "threshold" DOUBLE PRECISION NOT NULL,
    "result" TEXT NOT NULL,
    "riskLevel" TEXT NOT NULL,
    "modelType" TEXT NOT NULL,
    "modelVersion" TEXT NOT NULL,
    "featuresUsed" INTEGER NOT NULL,
    "engineeredFeatures" JSONB NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "fraud_predictions_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "transactions_userId_idx" ON "transactions"("userId");

-- CreateIndex
CREATE UNIQUE INDEX "fraud_predictions_transactionId_key" ON "fraud_predictions"("transactionId");

-- AddForeignKey
ALTER TABLE "transactions" ADD CONSTRAINT "transactions_userId_fkey" FOREIGN KEY ("userId") REFERENCES "users"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "fraud_predictions" ADD CONSTRAINT "fraud_predictions_transactionId_fkey" FOREIGN KEY ("transactionId") REFERENCES "transactions"("id") ON DELETE CASCADE ON UPDATE CASCADE;
