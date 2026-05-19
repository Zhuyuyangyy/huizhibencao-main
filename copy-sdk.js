// Auto-generated script to copy the iFlytek SDK file
const fs = require('fs');
const path = require('path');

const src = 'D:\\ZYY_Project\\huiben-qianduan-main\\huiben-qianduan-main\\src\\lib\\vm-sdk\\avatar-sdk-web_3.1.2.1002\\index-OS7Lza_r.js';
const dst = 'D:\\ZYY_Project\\huizhibencao\\huiben-qianduan-main\\src\\lib\\vm-sdk\\avatar-sdk-web_3.1.2.1002\\index-OS7Lza_r.js';

try {
  const content = fs.readFileSync(src);
  fs.writeFileSync(dst, content);
  console.log('SUCCESS: Copied ' + content.length + ' bytes');
} catch (e) {
  console.error('ERROR:', e.message);
}
