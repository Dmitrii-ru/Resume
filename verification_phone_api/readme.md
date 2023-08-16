# User Registration by Phone Number

## Request: POST /api/verification_phone/send_code

### Validation

- Check phone number format.
- Check phone number uniqueness.

### Functions

- Simulate code send delay.
- Generate code.
- Cache code.

### Response

- Confirmation code

---

# User Creation and Invitation Issuance

## Request: POST /api/verification_phone/invite_code

### Validation

- Check phone number format.
- Check phone number uniqueness.
- Check code presence in cache.

### Functions

- Create user.
- Generate invitation.
- Generate link to user profile.

### Response

- Link to user profile
- Invitation

---

# Invitation Activation

## Request: PUT /api/verification_phone/profile/<phone_number>

### Validation

- Check invitation existence.

### Functions

- Check profile existence.
- Check invitation activation.
- Activate invitation.

### Response

- User successfully activated invite

---

# List Invitations

## Request: GET /api/verification_phone/profile/<phone_number>

### Functions

- Check profile existence.
- Get a list of users who activated the invite of the current user.

### Response

- Profile
- List of invitations
