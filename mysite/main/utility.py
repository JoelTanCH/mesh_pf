
def unit_convertor(param,value,source='mg/dl',target='mmol/l'):
    source=source.lower()
    target=target.lower()
    print('DD:convertor',param,value,source,target,type(value))
    if value==None:
        return None
    if source==target:
        return value

    if isinstance(value,str):
        value_lower=value.lower().strip()
        if value_lower.find('reactive')>=0 or value_lower.find('positive')>=0 or value_lower.find('negative')>=0:
            return value.lower()

    # If there is no ouput unit or the unit is qualitative, do no conversion
    if source in ['','+ve/-ve'] or target in ['','+ve/-ve']:
        return value

    xsign=''
    try:
        x=float(value)
        print('DD:convertor',param,value,source,target,type(x))
    except:
        #Can't convert to a float
        if isinstance(value,str):
            # Assumption: there isn't negative signs. else, we need to do a slight tweak to this function
            # If the string is something like "55-75"
            if "-" in value:
                value1 = value.split("-")[0].strip()
                value2 = value.split("-")[1].strip()
                return "{}-{}".format(unit_convertor(param, value1, source, target), unit_convertor(param, value2, source, target))
            try:
                xsign=re.findall('[><=-]+',value)[0]
                x=re.findall('[\d.]+',value)[0]
            except:
                #print('DD: param={}, value={}'.format(param,value))
                raise Exception


    if (source=='ug/l' and target=='ng/ml') or (target=='ug/l' and source=='ng/ml'):
        xnumeric=float(x)
    elif source=='g/l' and target=='g/dl':
        xnumeric=float(x)/10
    elif source=='g/dl' and target=='g/l':
        xnumeric=float(x)*10
    elif source=='ratio' and target=='%':
        xnumeric=float(x)*100
    elif source=='%' and target=='ratio':
        xnumeric=round((float(x)/100),2)
    elif param in ["totalCholesterol", "highDensityLipidCholesterol", "lowDensityLipidCholesterol"]:
        if source=='mg/dl' and target == 'mmol/l':
            xnumeric=float(x)/38.67
        elif source=='mmol/l' and target == 'mg/dl':
            xnumeric=float(x)*38.67
        else:
            xnumeric=float(x)
    elif param == "triglycerides":
        if source=='mg/dl' and target == 'mmol/l':
            xnumeric=float(x)/88.57
        elif source=='mmol/l' and target == 'mg/dl':
            xnumeric=float(x)*88.57
        else:
            xnumeric=float(x)
    elif param == 'glucose':
        if source=='mg/dl' and target == 'mmol/l':
            xnumeric=float(x)/18
        elif source=='mmol/l' and target == 'mg/dl':
            xnumeric=float(x)*18
        else:
            xnumeric=float(x)
    elif param == 'hba1c':
        if source=='mmol/mol' and target == '%':
            xnumeric=(float(x)/10.929+2.15)
        elif source=='%' and target == 'mmol/mol':
            xnumeric=(float(x)-2.15)*10.929
        else:
            xnumeric=float(x)
    elif param == 'height':
        if source=='m' and target == 'cm':
            xnumeric=round((float(x)*100),3)
        elif source=='cm' and target == 'm':
            xnumeric=round((float(x)/100),3)
        else:
            xnumeric=float(x)
    elif param == 'albuminuria':
        if source=='mg/mmol' and target == 'mg/g':
            xnumeric=float(x)*8.84
        elif source=='mg/g' and target == 'mg/mmol':
            xnumeric=float(x)/8.84
        else:
            xnumeric=float(x)
    elif param in ['totalBilirubin', 'directBilirubin', 'indirectBilirubin']:
        if source=='mg/dl' and target=='umol/l':
            xnumeric=float(x)*17.1
        elif target=='mg/dl' and source=='umol/l':
            xnumeric=float(x)/17.1
        else:
            xnumeric=float(x)
    elif param in ['potassium','chloride','lithium','sodium']:
        if source=='mmol/l' and target=='meq/l':
            xnumeric=float(x)*1.0
        elif target=='mmol/l' and source=='meq/l':
            xnumeric=float(x)*1.0
        else:
            xnumeric=float(x)
    elif param=='urea':
        if source=='mmol/l' and target == 'mg/dl':
            xnumeric=float(x)*6.006
        elif target=='mmol/l' and source == 'mg/dl':
            xnumeric=float(x)/6.006
        else:
            xnumeric=float(x)
    elif param=='uricAcid':
        if source=='mmol/l' and target == 'mg/dl':
            xnumeric=float(x)*16.811
        elif target=='mmol/l' and source == 'mg/dl':
            xnumeric=float(x)/16.811
        else:
            xnumeric=float(x)
    elif param=='calcium':
        if source=='mmol/l' and target == 'mg/dl':
            xnumeric=float(x)*4.0088
        elif target=='mmol/l' and source == 'mg/dl':
            xnumeric=float(x)/4.0088
        else:
            xnumeric=float(x)
    elif param=='inorganicPhosphate':
        if source=='mmol/l' and target == 'mg/dl':
            xnumeric=float(x)*3.1
        elif target=='mmol/l' and source == 'mg/dl':
            xnumeric=float(x)/3.1
        else:
            xnumeric=float(x)
    elif param=='creatinine':
        if source=='mmol/l' and target == 'mg/dl':
            xnumeric=float(x)*11.312
        elif target=='mmol/l' and source == 'mg/dl':
            xnumeric=float(x)/11.312
        elif source=='mg/dl' and target == 'umol/l':
            xnumeric=round((float(x)*88.42),1)
        elif target=='mg/dl' and source == 'umol/l':
            xnumeric=round((float(x)/88.422),1)
        else:
            xnumeric=float(x)
    elif param=='albumin':
        if source=='mmol/l' and target == 'g/l':
            xnumeric=float(x)*66.46
        elif source=='mmol/l' and target == 'g/dl':
            xnumeric=float(x)*6.646
        elif target=='mmol/l' and source == 'g/l':
            xnumeric=float(x)/66.46
        elif target=='mmol/l' and source == 'g/dl':
            xnumeric=float(x)/6.646
        else:
            xnumeric=float(x)
    elif param=='globulin':
        if source=='g/dl' and target == 'g/l':
            xnumeric=float(x)*10
        elif target=='g/dl' and source == 'g/l':
            xnumeric=float(x)/10
        else:
            xnumeric=float(x)
    elif param=='wrCRP':
        if source=='nmol/l' and target == 'mg/l':
            xnumeric=float(x)*0.105
        elif target=='nmol/l' and source == 'mg/l':
            xnumeric=float(x)/0.105
        else:
            xnumeric=float(x)
    elif param=='urineMicroAlbumin':
        if source=='mg/l' and target == 'ug/ml':
            xnumeric=float(x)
        elif target=='mg/l' and source == 'ug/ml':
            xnumeric=float(x)
        else:
            xnumeric=float(x)
    elif param=='folicAcid':
        if source=='nmol/l' and target == 'ng/dl':
            xnumeric=float(x)*44
        elif target=='nmol/l' and source == 'ng/dl':
            xnumeric=float(x)/44
        elif source=='nmol/l' and target == 'ng/ml':
            xnumeric=float(x)*0.44
        elif target=='nmol/l' and source == 'ng/ml':
            xnumeric=float(x)/0.44
        else:
            xnumeric=float(x)
    elif param=='vitB12':
        if source=='pmol/l' and target == 'pg/ml':
            xnumeric=float(x)*1.3554
        elif target=='pmol/l' and source == 'pg/ml':
            xnumeric=float(x)/1.3554
        elif source=='pmol/l' and target == 'pg/dl':
            xnumeric=float(x)*135.537
        elif target=='pmol/l' and source == 'pg/dl':
            xnumeric=float(x)/135.537
        else:
            xnumeric=float(x)
    elif param=='t4':
        if source=='pmol/l' and target=='ng/dl':
            xnumeric=float(x)*0.0777
        elif target=='pmol/l' and source=='ng/dl':
            xnumeric=float(x)/0.0777
        elif source=='pmol/l' and target=='pg/ml':
            xnumeric=float(x)*0.7767
        elif target=='pmol/l' and source=='pg/ml':
            xnumeric=float(x)/0.7767
        else:
            xnumeric=float(x)
    elif param=='t3':
        if source=='pmol/l' and target=='ng/dl':
            xnumeric=float(x)*0.0651
        elif target=='pmol/l' and source=='ng/dl':
            xnumeric=float(x)/0.0651
        elif source=='pmol/l' and target=='pg/ml':
            xnumeric=float(x)*0.651
        elif target=='pmol/l' and source=='pg/ml':
            xnumeric=float(x)/0.651
        else:
            xnumeric=float(x)
    elif param=='testosterone':
        if source=='nmol/l' and target=='ng/dl':
            xnumeric=float(x)*28.842
        elif target=='nmol/l' and source=='ng/dl':
            xnumeric=float(x)/28.842
        elif source=='nmol/l' and target=='ng/ml':
            xnumeric=float(x)*0.2884
        elif target=='nmol/l' and source=='ng/ml':
            xnumeric=float(x)/0.2884
        else:
            xnumeric=float(x)
    elif param=='height':
        if source=='m' and target=='cm':
            xnumeric=float(x)*100
        elif target=='m' and source=='cm':
            xnumeric=float(x)/100
        else:
            xnumeric=float(x)
    elif param=='urineSpecificGravity':
        if source=='g/cm3' and target=='kg/L':
            xnumeric=float(x)
        elif target=='g/cm3' and source=='kg/L':
            xnumeric=float(x)
        else:
            xnumeric=float(x)
    elif param=='vitaminD':
        if source=='nmol/l' and target=='ng/ml':
            xnumeric=round((float(x)/2.5),2)
        elif target=='nmol/l' and source=='ng/ml':
            xnumeric=round((float(x)*2.5),2)
        else:
            xnumeric=float(x)
    elif param=='dehydroepiandrosteroneSulfate':
        if source=='umol/l' and target=='ug/dl':
            xnumeric=float(x)*37
        elif target=='umol/l' and source=='ug/dl':
            xnumeric=float(x)/37
        else:
            xnumeric=float(x)
    elif param=='antiMullerianHormone':
        if source=='pmol/l' and target=='ng/ml':
            xnumeric=float(x)*0.14
        elif target=='pmol/l' and source=='ng/ml':
            xnumeric=float(x)/0.14
        else:
            xnumeric=float(x)
    else:
        xnumeric=x

    print('DD:convertor:converted',param,value,source,target,type(x),xnumeric,xsign)
    if len(xsign)>0:
        return '{}{}'.format(xsign,xnumeric)
    else:
        return xnumeric