import label_dir as ld
import getData_uc as gd
from os import path
import operator

def GoToOnNowGuide(imageFolder = '3'):
    fullFolder = path.join(path.dirname(path.realpath(__file__)), imageFolder)
    gd.to_guide(imageFolder)
    predictions = ld.images_predictions(fullFolder)
    result = AnalysisPrediction(predictions)
    print(GenerateReportPage(result, imageFolder))

def AnalysisPrediction(predictions):
    throshold = 0.60
    loadingOnNow_id = -1
    OnNow_id = -1
    ret = []
    for i, page in enumerate(predictions):
        if predictions[i][1][0][3] > throshold:
            loadingOnNow_id = i
            break
    #print("Loading OnNow:" + predictions[loadingOnNow_id][0])
    ret.append(predictions[loadingOnNow_id])
    while i < len(predictions):
        if predictions[i][1][0][0] > throshold:
            OnNow_id = i
            break
        i = i+1
    print("OnNow Guide:" + predictions[OnNow_id][0])
    ret.append(predictions[OnNow_id])
    loadingFull_id = -1
    while i < len(predictions):
        if predictions[i][1][0][4] > throshold:
            loadingFull_id = i
            break
        i = i+1
    #print("Loading FullGuide:" + predictions[loadingFull_id][0])
    ret.append(predictions[loadingFull_id])
    fullguide_id = -1
    while i < len(predictions):
        if predictions[i][1][0][1] > throshold:
            fullguide_id = i
            break
        i = i+1
    print("FullGuide:" + predictions[fullguide_id][0])
    ret.append(predictions[fullguide_id])

    return ret

def GenerateReportPage(pagePredictions, imagePath):
    html = '<html><body><table><tr><td>image</td><td>predictions - onnowguide, fullguide, error, loadingonnow, loadingfullguide</td><td>page</td><td>description</td></tr>'
    pages = ['Loading OnNow', 'OnNow Guide', 'Loading Full Guide', 'Full Guide']
    framerate = 59.96
    for i,p in enumerate(pages):
        t_desc = ''
        if i%2==1:
            pagename = pagePredictions[i][0]
            frame_id =  int(pagename[-8:-4])
            t_desc = '{0:.2f} senconds'.format(frame_id / framerate)

        html += append_line(pagePredictions[i][0], pagePredictions[i][1][0], p, imagePath, t_desc)
    html += '</table></body></html>'
    return html

def append_line(imageFile, prediction_values, pagename, imagePath, desc):
    return '<tr><td><image width=\'400\' src=\'{}\\{}\'/></td><td>{}</td><td>{}</td><td>{}</td></tr>'.format(imagePath, imageFile, prediction_values, pagename, desc)






