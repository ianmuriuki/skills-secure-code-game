#ifndef CODE_H
#define CODE_H

#include <stdbool.h>

#define MAX_USERNAME_LEN 39
#define SETTINGS_COUNT 10
#define MAX_USERS 100
#define INVALID_USER_ID -1

// Define a structure for user accounts
typedef struct {
    bool isAdmin;
    long userid;
    char username[MAX_USERNAME_LEN + 1];
    long setting[SETTINGS_COUNT];
} user_account;

// Internal counter of user accounts
extern int userid_next;

// Simulates an internal store of active user accounts
extern user_account *accounts[MAX_USERS];

// Function declarations

// Creates a new user account and returns its unique identifier
int create_user_account(bool isAdmin, const char *username);

// Updates the matching setting for the specified user and returns the status of the operation
// A setting is some arbitrary string associated with an index as a key
bool update_setting(int user_id, const char *index, const char *value);

// Returns whether the specified user is an admin
bool is_admin(int user_id);

// Returns the username of the specified user
const char* username(int user_id);

#endif
