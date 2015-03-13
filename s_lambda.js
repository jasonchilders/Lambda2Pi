/**
 * Created by jchilders on 2/28/15.
 */

S = function(x) {
        return function(y) {
            return function(z) {
                return x(z)(y(z))
            }
        }
    };

print(S(4));
x = 1;





