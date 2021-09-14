# encoding:utf-8
import execjs

js = execjs.compile('''function T() {
            var a = (new Date).getTime();
            var b = "xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx".replace(/[xy]/g, function(b) {
                var c = (a + 16 * Math.random()) % 16 | 0;
                return a = Math.floor(a / 16),
                ("x" == b ? c : 3 & c | 8).toString(16)
            });
            return b
        }''')

if __name__ == '__main__':
    result = js.call('T')
    print(result)






