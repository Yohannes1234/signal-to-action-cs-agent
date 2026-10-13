const DRIVER_LABELS = {
  support_activity: "Support activity",
  nps: "Customer sentiment (NPS)",
  usage_trend: "Usage trend",
  engagement_recency: "Engagement recency",
  none: "None (no elevated risk)",
};

export function driverLabel(driver) {
  return DRIVER_LABELS[driver] || driver;
}