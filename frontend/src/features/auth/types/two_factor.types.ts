export interface TwoFactorSetupResponse {
  secret: string;
  qr_code: string;
  manual_entry_key: string;
}

export interface TwoFactorStatusResponse {
  enabled: boolean;
}

export interface TwoFactorEnableResponse {
  success: boolean;
  message: string;
  backup_codes: string[];
}
