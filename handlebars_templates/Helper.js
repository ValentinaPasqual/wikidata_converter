	'allNormals': function(arg) { 
		for (var i in arg) {
			if (arg[i].rank !== 'normal')
				return false
		}
		return true
	},
	'hasDeprecated': function(arg) { 
		for (var i in arg) {
			if (arg[i].rank == 'deprecated')
				return true
		}
		return false
	},
	'hasPreferred': function(arg) { 
		for (var i in arg) {
			if (arg[i].rank == 'preferred')
				return true
		}
		return false
	},
	'isDeprecated': function(arg) { return arg.rank == 'deprecated' },
	'isNormal': function(arg) { return arg.rank == 'normal' },
	'isPreferred': function(arg) { return arg.rank == 'preferred' }
