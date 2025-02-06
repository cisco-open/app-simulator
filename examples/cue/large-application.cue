import "list"
import "math"

#depth: int @tag(depth,type=int)
#adjectives: ["swift", "happy", "brave", "clever", "silent", "bold", "lucky", "fierce", "gentle", "mighty", "shy", "curious", "wise", "playful", "proud", "loyal"]
#nouns: ["lion", "tiger", "eagle", "panda", "fox", "wolf", "hawk", "bear", "otter", "falcon", "rabbit", "panther", "deer", "owl", "cheetah", "dolphin"]

loaders: {
	"user1": {
		type: "curl",
		wait: 5,
		sleep: 2,
		urls: [ "http://swift-lion/next" ] 
	}
}

services: {
	for x in list.Range(0, #depth+1, 1) {
		for y in list.Range(0, x+1, 1) {
			"\(#adjectives[x])-\(#nouns[y])": {
				type: "java"
				endpoints: {
					http: {
							    "/next": list.Concat([[
        for i in [y, y+1] if x < #depth {
            "http://\(#adjectives[x+1])-\(#nouns[i])/next"
        }
    ], ["sleep,\(math.Exp2(x)+(y*10))"]])
					}
				}
			}
		}
	}
}
