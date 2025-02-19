#include "code.h"
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>

// Internal counter for the next user id
int userid_next = 0;

// Array to store user accounts
user_account *accounts[MAX_USERS];

// Function to create a new user account
int create_user_account(bool isAdmin, const char* username) {
    if (userid_next >= MAX_USERS) {
        fprintf(stderr, "Maximum user limit reached.\n");
        return INVALID_USER_ID;
    }
    
    // Allocate memory for the new user account
    user_account *ua = malloc(sizeof(user_account));
    if (ua == NULL) {
        fprintf(stderr, "Failed to allocate memory for the new user account.\n");
        return INVALID_USER_ID;
    }

    // Set the user details
    ua->isAdmin = isAdmin;
    ua->userid = userid_next++;
    strncpy(ua->username, username, MAX_USERNAME_LEN);
    ua->username[MAX_USERNAME_LEN] = '\0'; // Ensure null-termination for the username

    // Initialize settings to 0
    memset(ua->setting, 0, sizeof(ua->setting));

    // Store the user in the accounts array
    accounts[ua->userid] = ua;

    return ua->userid;
}

// Function to update user settings (example)
bool update_setting(int user_id, const char* index, const char* value) {
    if (user_id < 0 || user_id >= MAX_USERS) {
        fprintf(stderr, "Invalid user ID\n");
        return false;
    }

    char *endptr;
    long i = strtol(index, &endptr, 10);
    if (*endptr || i < 0 || i >= SETTINGS_COUNT) {
        fprintf(stderr, "Invalid setting index\n");
        return false;
    }

    long v = strtol(value, &endptr, 10);
    if (*endptr) {
        fprintf(stderr, "Invalid value for setting\n");
        return false;
    }

    accounts[user_id]->setting[i] = v;
    return true;
}

// Function to check if a user is an admin
bool is_admin(int user_id) {
    if (user_id < 0 || user_id >= MAX_USERS) {
        fprintf(stderr, "Invalid user ID\n");
        return false;
    }
    return accounts[user_id]->isAdmin;
}

// Function to get the username of a user
const char* username(int user_id) {
    if (user_id < 0 || user_id >= MAX_USERS) {
        fprintf(stderr, "Invalid user ID\n");
        return NULL;
    }
    return accounts[user_id]->username;
}
