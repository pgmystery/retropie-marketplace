# RetroPie Marketplace Framework

⚠️ **Legal Disclaimer**

This project provides a **framework** for managing and installing game ROMs on RetroPie. It **does not include or promote any copyrighted material**.

Users are responsible for ensuring that all content downloaded or installed using this tool complies with local copyright laws. This framework is intended for use with **legal content only**, such as:

- Homebrew games
- Public domain ROMs
- Personal backups of games you own (where legally permitted)

This project **does not condone or facilitate piracy** in any form.

---

## Usage Notes

- The framework is designed to be **extensible**, allowing users to add their own scrapers or download modules.
- No scrapers or downloaders for unauthorized or copyrighted ROM sites are included.
- Users should add and maintain any custom scrapers locally and at their own risk.

---

## Getting Started

```
wget https://github.com/pgmystery/retropie-marketplace/archive/master.zip -P /tmp/ && unzip /tmp/master.zip -d /tmp/ && python /tmp/retropie-marketplace-master/marketplace/setup.py && rm -rf master.zip && rm -rf retropie-marketplace-master
```

---

## Contributing

Contributions that promote only legal usage are welcome. Please avoid adding scrapers or modules that connect to unauthorized ROM repositories.
