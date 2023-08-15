
# Getting a code for registering a user by phone number.
## POST api/verification_phone/send_code

## REQUEST


### Validate
#### validate_phone_number
- Checking the format phone_number.
- Check for uniqueness of phone number.

### Function
- Simulate code send delay.
- Code generation.
- Code caching. 

## RESPONSES
- Return code


---

# Create user into the database and issue invite.
## POST api/verification_phone/invite_code

## REQUEST

### Validate
#### validate_phone_number
- Checking the format phone number.
- Check for uniqueness of phone number.

#### validate_code
- Checking the cache for the presence of a phone number and validata code

### Function
- Create user
- Invite generation
- Generation link user profile

## RESPONSES
- Link to profile
- invite

---

# Invite activation
## PUT api/verification_phone/profile/<phone_number>

## REQUEST
- api/verification_phone/profile/+7(999)999-99-99


### Validate

#### validate
- Check for the existence of invite.

### Function
- Check for existence profile.
- Check invite activation.
- Invite activation.


## RESPONSES
- "message": f"{user} successfully activated invite"

---
# Внесение  invite
## GET api/verification_phone/profile/<phone_number>

## REQUEST



### Function
- Check for existence profile.
- Get a list of users who activated the invite of the current user

## RESPONSES
- Profile
- List invite

