function getUserId(Ionic) {
	return '90bc5b12-42ab-4dfb-8b5c-df306fef8471'; // fix to be me.

	// kick off the platform web client
	Ionic.io();

	// this will give you a fresh user or the previously saved 'current user'
	var user = Ionic.User.current();

	// if the user doesn't have an id, you'll need to give it one.
	if (!user.id) {
	  user.id = Ionic.User.anonymousId();
	  // user.id = 'your-custom-user-id';
	}

	//persist the user
	user.save();

	return user.id;
}