const fs = require('fs');
const axios = require('axios');




function processFile(path) {
    fs.readFile(path, 'utf8', async function(err, data) {
        if (err) {
            console.error("ERROR", err);
            process.exit(1);
        }
        let urls = data.split('\n').filter(u => u !== '');
        for (let url of urls) {
            let resp;

            try {
                resp = await axios.get(url);
            } catch {
                console.error(`couldn't download`);
                continue;
            }

            let fileName = new URL(url).hostname;

            fs.writeFile(fileName, resp.data, 'utf8', function(err) {
                if (err) {
                    console.error(`couldn't write`);
                }
                console.log(`done writing`);
            });
        }
    });   
}

processFile(process.argv[2]);