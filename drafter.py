def get_bank_dispute_draft(user_name, bank_name, amount, transaction_id, date):
    return f"""Subject: URGENT: Fraudulent Transaction Dispute (Action Required) - {user_name}

To,
The Nodal Officer / Branch Manager,
{bank_name}

Ref: Unauthorized Transaction of INR {amount} on {date}

Respected Sir/Madam,

I am writing to formally report an unauthorized and fraudulent transaction on my bank account/credit card with your bank.

Incident Details:
- Account Name: {user_name}
- Transaction Amount: INR {amount}
- Date & Time: {date}
- Transaction ID/Reference: {transaction_id}
- Incident Type: Financial Internet Fraud (USW)

I confirm that I did NOT authorize this transaction. I have neither shared my OTP, PIN, nor password with anyone knowingly. This transaction appears to be a result of a cybercrime incident.

As per RBI guidelines on 'Customer Protection ? Limiting Liability of Customers in Unisuthorised Electronic Banking Transactions', I am reporting this within the stipulated time.

Immediate Action Requested:
1. Block my affected card/account immediately to prevent further loss.
2. Initiate a chargeback/dispute for the above transaction ID.
3. Credit the amount back to my account on a temporary basis pending investigation.
4. Provide an acknowledgment number for this complaint.

I am also filing a complaint with the National Cybercrime Portal (1930) and local police.

Sincerely,
{user_name}
(Registered Mobile Number)"""

def get_police_complaint_draft(user_id, incident_type, date, details):
    return f"""Subject: Information/Complaint regarding Cybercrime Incident ({incident_type})

To,
The Station House Officer (SHO),
Cyber Crime Police Station / Local Police Station,

Respected Sir/Madam,

I wish to report a cybercrime incident committed against me. I request you to register my complaint and take necessary legal action.

Complainant Details:
- Report ID (CyberRescue): {user_id}
- Date of Incident: {date}

Incident Narrative:
{details}

I request you to:
1. Register an FIR under relevant sections of the IT Act and IPC.
2. Investigate the IP addresses/Phone numbers involved.
3. Help me recover my lost funds/account access.

I have preserved all digital evidence (screenshots, transaction receipts) and have attached them herewith.

Yours Faithfully,
(Signature)
Name: ______________________
Mobile: ______________________
Address: _____________________"""

def get_social_media_appeal(platform, username, date):
    return f"""Subject: Hacked Account Recovery Appeal - @{username}

To,
The Trust & Safety Team,
{platform}

My account handle: @{username}
Date of Compromise: {date}

Dear Support Team,

I am the original owner of the account @{username}. I have lost access to my account, and I believe it was compromised/hacked on {date}.

Security Context:
- I suspect the hacker has changed my password and recovery email.
- Two-Factor Authentication (2FA) was [Enabled/Disabled] before the hack.
- I possess the original device used to access this account.

The current user of the account is impersonating me/misusing my data. I can provide Government ID proof or previous login history to verify my ownership.

Please send me a secure login link or revert my account settings to the state prior to {date}.

Thank you,
(Your Full Name)"""
