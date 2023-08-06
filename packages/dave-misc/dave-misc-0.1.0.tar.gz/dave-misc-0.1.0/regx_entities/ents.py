import re
import helpers as hp

class CanonicalFunctionError(Exception):
    pass

class FormaterFunctionError(Exception):
    pass

class RegxEntities:
    def __init__(self):
        self.__patterns = {}
        self.___defaults()

    def add_entity(self, key, pattern, canonical=None, formater=None, priority=False):
        
        if canonical and not callable(canonical):
            raise CanonicalFunctionError("Canonical parameter should be a function") 

        if formater and not callable(formater):
            raise FormaterFunctionError("Formater parameter should be a function")

        self.__patterns[key] = {
            "pattern": pattern,
            "canonical": canonical,
            "formater": formater,
            "priority": priority
        }



    def ___defaults(self):
        def to_aadhar(x):
            x= x.replace(" ", "").replace("-", "").replace(".", "")
            return " ".join(x[4*i: (4*i) +4] for i in range(3))
        
        def to_phone(x):
            x= x.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace(".", "")
            if x.startswith("00"):
                return "+{}".format(x[2:])
            return x
        def format_mobile(x):
            _x=x
            c = {}
            ls = re.findall(r"(double\s?\d\s?)", x)
            for se in ls:
                x = x.replace(se, re.findall(r"\d", se)[0]*2)
                c[re.findall(r"\d", se)[0]*2] = "".join(se.split())
            ls = re.findall(r"(triple\s?\d\s?)", x)
            for se in ls:
                x = x.replace(se, re.findall(r"\d", se)[0]*3)
                c[re.findall(r"\d", se)[0]*3] = "".join(se.split())
            ls = re.findall(r"\d\s\d", x)
            for se in ls:
                x = x.replace(se, "".join(re.findall(r"\d", se)))
            return x,_x,c

        def to_email(x):
            for p,r in ({" at the rate ": "@"," at ": "@", " dot ": "."}).items():
                x = x.replace(p, r)
            x = x.replace(" ", ".")
            return x
        
        def datetime_canonical(x):
            try:
                x = x.replace(" . ", ":")
                return hp.to_datetime(x, fuzzy=True).strftime('%Y-%m-%d %H:%M')
            except:
                return ""


        self.add_entity(
            "uid", 
            r'[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}'
        )

        self.add_entity(
            "alpha_numeric", 
            r"(([a-zA-Z]+[0-9]+[a-zA-Z]*)|([0-9]+[a-zA-Z]+[0-9]*))+"
        )

        self.add_entity(
            "number", 
            r"[0-9]+(\s[0-9]+)*",
            canonical=lambda x: x.replace(" ", "")
        )

        self.add_entity(
            "aadhar", 
            r"[0-9]{12}$|((([0-9]{4}(\s)){2})|(([0-9]{4}(-)){2})|(([0-9]{4}(\.)){2}))[0-9]{4}",
            canonical=to_aadhar,
            priority=True
        )

        self.add_entity(
            "pan_number", 
            r"([A-Za-z]\s?){5}([0-9]\s?){4}[A-Za-z]",
            canonical=lambda x: x.replace(" ", "")
        )

        self.add_entity(
            "vehicle_number", 
            r"[A-Za-z]{2}[\s\-\.\_]?[0-9]{1,2}[\s\-\.\_]?[A-Za-z]{1,3}[\s\-\.\_]?[0-9]{2,4}",
            canonical=lambda x: (x.replace(z, "") for z in ["-",".", "_"," "])
        )

        self.add_entity(
            "pincode", 
            r"[0-9]{6}",
            canonical=lambda x: x.replace(" ", ""),
            priority=True
        )

        self.add_entity(
            "email", 
            r"[a-zA-Z]{1}([\w-]+(\.|\-))*[\w]+(@|\sat\s|\sat\sthe\srate\s){1}([\w-]+(\.|\sdot\s|\s))+[\w-]{2,4}",
            canonical=to_email,
            priority=True
        )

        self.add_entity(
            "phone_number", 
            r"([0]|((\+|00)91[\s\-\.]?)|\((\+|00)?91\)\s?)?(\d{10}|\d{5}[\s\-\.]?\d{5,6}|\d{3}[\s\-\.]?\d{3}[\s\-\.]?\d{4,5}|\(\d{4}\)[\s\-\.]?\d{3}[\s\-\.]?\d{3,4}|\(\d{3}\)[\s\-\.]?\d{3}[\s\-\.]?\d{4,5}|\d{2}[\s\-\.]?\d{3}[\s\-\.]?\d{6})",
            canonical=to_phone,
            formater=format_mobile,
            priority=True
        )

        self.add_entity(
            "datetime", 
            r"(([0-9]{1,2}\/{1}([0-9]{1,2}|[a-z]{3,})\/(20|19)?[0-9]{2})|([0-9]{1,2}\-([0-9]{1,2}|[a-z]{3,})\-(20|19)?[0-9]{2}))?\s?([0-9]{1,2}\s?[\:\.]\s?[0-9]{1,2}\s?((a|A|p|P)[\.\s]?(m|M)[\.\s]?)?)?",
            canonical=datetime_canonical,
            priority=True
        )
    
    def get_matchs(self, otext, pre=None):
        pre = pre or []
        ind = len(pre)

        def formatter_word_match(s1, s2, replables):
            for i,j in replables.items():
                s2 = s2.replace(i, j)

            s1 = s1.split() 
            s2 = s2.split() 
            if len(s1) == len(s2): 
                return {} 
            s3 = [] 
            c_map = {}  
            i2 = 0 
            for i in range(len(s1)):  
                if s1[i] == s2[i2]: 
                    i2+=1 
                    continue 
                else:  
                    s3.append(s1[i]) 
                if s2[i2] == "".join(s3):
                    ky = s2[i2]
                    for j,k in replables.items():
                        ky = ky.replace(k,j)
                    c_map[ky] = " ".join(s3)
                    i2+=1
            return c_map 

        for i, pt in self.__patterns.items():
            patt = pt
            canonical_fun = None
            formater_fun = None
            text_ = otext
            priority_ = False
            can_map = {}
            if isinstance(pt, dict):
                patt = pt["pattern"]
                canonical_fun = pt.get("canonical")
                formater_fun = pt.get("formater")
                priority_ = pt.get("priority", False)
    
            text = otext
            if formater_fun:
                text, text_,rpl = formater_fun(otext)
                can_map = formatter_word_match(text_,text, rpl)
                
            patt = r"(^|\s){}(\s|$)".format(patt)
            ls = re.finditer(patt, otext)
            for t in ls:
                word = text[t.span()[0]:t.span()[1]]
                si, ei = t.span()[0], t.span()[1]
                word = word[1:] if word[0] == " " else word
                canonical = word
                if canonical_fun:
                    canonical = canonical_fun(word)
                fl = False
                for z in pre:
                    if (z["word"] in canonical or z["word"] in word) or ( word in z["word"] or canonical in z["word"]):
                        fl= True
                        if z.get("priority", False):
                            continue
                        if priority_:
                            if len(z["word"]) < len(word):
                                z["word"] = can_map.get(canonical, word)
                            z["probs"] = {i: 1.0}
                            z["priority"] = True
                        else:
                            z["probs"][i] = 1.0
                        z["class"] = max(z["probs"], key=z["probs"].get)
                        z["canonical"] = canonical
                        
                        break

                if not fl:
                    ob = {
                        "index": ind,
                        "word": can_map.get(canonical, word),
                        "class": i,
                        "probs": {},
                        "canonical": canonical,
                        "priority": priority_,
                        "start_index": si,
                        "end_index": ei
                    }
                    ind = ind + 1

                    ob["probs"][i] = 1.0
                    
                    pre.append(ob)
                """
                if canonical:
                    ind = ind + 1
                    ob = {
                        "index": ind,
                        "word": canonical,
                        "class": i,
                        "probs": {},
                        "actual_word": word
                    }
                    ob["probs"]["{}_canonical".format(i)] = 1.0
                    pre.append(ob)
                """

        return pre