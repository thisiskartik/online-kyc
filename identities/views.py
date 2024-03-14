import re
import boto3
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from identities.models import Identity
from identities.serializers import IdentitySerializer


@api_view(['POST'])
def upload_face_image(request, identity_id):
    face_img = request.FILES['face']
    extension = face_img.name.split('.')[-1].lower()
    filename = identity_id + '.' + extension

    session = boto3.Session()
    s3 = boto3.resource('s3')
    face_obj = s3.Object('aadhar-kyc-hackathon', f"face/{filename}")
    face_obj.put(Body=face_img, Key=f"face/{filename}")

    client = session.client('rekognition')
    response = client.detect_labels(
        Image={'S3Object':
            {
                'Bucket': 'aadhar-kyc-hackathon',
                'Name': f"face/{filename}"
            }
        },
        MaxLabels=10,
        Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        Settings={
            "GeneralLabels": {
                "LabelInclusionFilters": ["Face"]
            }
        }
    )

    confidence = 0
    for label in response['Labels']:
        if label['Name'] == 'Face':
            confidence = label['Confidence']

    if confidence < 95:
        return Response({'error': 'Face not detected'})
    else:
        identity = Identity.objects.get(id=identity_id)
        identity.face_image = f"https://aadhar-kyc-hackathon.s3.ap-south-1.amazonaws.com/face/{filename}"
        identity.save()
        return Response(IdentitySerializer(identity).data, HTTP_200_OK)


@api_view(['POST'])
def upload_signature_image(request, identity_id):
    face_img = request.FILES['signature']
    extension = face_img.name.split('.')[-1].lower()
    filename = identity_id + '.' + extension

    session = boto3.Session()
    s3 = boto3.resource('s3')
    face_obj = s3.Object('aadhar-kyc-hackathon', f"signature/{filename}")
    face_obj.put(Body=face_img, Key=f"signature/{filename}")

    client = session.client('rekognition')
    response = client.detect_labels(
        Image={'S3Object':
            {
                'Bucket': 'aadhar-kyc-hackathon',
                'Name': f"signature/{filename}"
            }
        },
        MaxLabels=10,
        Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        Settings={
            "GeneralLabels": {
                "LabelInclusionFilters": ["Signature"]
            }
        }
    )

    confidence = 0
    for label in response['Labels']:
        if label['Name'] == 'Signature':
            confidence = label['Confidence']

    if confidence < 95:
        return Response({'error': 'Signature not detected'})
    else:
        identity = Identity.objects.get(id=identity_id)
        identity.signature_image = f"https://aadhar-kyc-hackathon.s3.ap-south-1.amazonaws.com/signature/{filename}"
        identity.save()
        return Response(IdentitySerializer(identity).data, HTTP_200_OK)


@api_view(['POST'])
def upload_aadhar_image(request, identity_id):
    face_img = request.FILES['aadhar']
    extension = face_img.name.split('.')[-1].lower()
    filename = identity_id + '.' + extension

    session = boto3.Session()
    s3 = boto3.resource('s3')
    face_obj = s3.Object('aadhar-kyc-hackathon', f"aadhar/{filename}")
    face_obj.put(Body=face_img, Key=f"aadhar/{filename}")

    client = session.client('rekognition')
    response = client.detect_labels(
        Image={'S3Object':
            {
                'Bucket': 'aadhar-kyc-hackathon',
                'Name': f"aadhar/{filename}"
            }
        },
        MaxLabels=10,
        Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        Settings={
            "GeneralLabels": {
                "LabelInclusionFilters": ["Document"]
            }
        }
    )

    detection_confidence = 0
    for label in response['Labels']:
        if label['Name'] == 'Document':
            detection_confidence = label['Confidence']

    comparison_similarity = 0
    try:
        identity = Identity.objects.get(id=identity_id)
        response = client.compare_faces(SourceImage={'S3Object': {
                                 "Bucket": "aadhar-kyc-hackathon",
                                 "Name": f"aadhar/{filename}"
                             }},
                             TargetImage={'S3Object': {
                                 "Bucket": "aadhar-kyc-hackathon",
                                 "Name": identity.face_image.split("amazonaws.com/")[-1]
                             }})

        comparison_similarity = response['FaceMatches'][0]['Similarity']
    except:
        return Response({'error': 'Invalid aadhar card'})

    aadhar_number = ""
    try:
        response = client.detect_text(Image={'S3Object': {
            "Bucket": "aadhar-kyc-hackathon",
            'Name': f"aadhar/{filename}"}})
        for text in response['TextDetections']:
            detected_text = text['DetectedText']
            pattern = re.compile("^\d{4} \d{4} \d{4}$")
            if pattern.match(detected_text):
                aadhar_number = detected_text
    except:
        return Response({'error': 'Invalid aadhar card'})

    if detection_confidence < 95 or comparison_similarity < 95:
        return Response({'error': 'Invalid aadhar card'})
    else:
        identity.aadhar_image = f"https://aadhar-kyc-hackathon.s3.ap-south-1.amazonaws.com/aadhar/{filename}"
        identity.aadhar_number = aadhar_number
        identity.save()
        return Response(IdentitySerializer(identity).data, HTTP_200_OK)


@api_view(['POST'])
def upload_pan_image(request, identity_id):
    face_img = request.FILES['pan']
    extension = face_img.name.split('.')[-1].lower()
    filename = identity_id + '.' + extension

    session = boto3.Session()
    s3 = boto3.resource('s3')
    face_obj = s3.Object('aadhar-kyc-hackathon', f"pan/{filename}")
    face_obj.put(Body=face_img, Key=f"pan/{filename}")

    client = session.client('rekognition')
    response = client.detect_labels(
        Image={'S3Object':
            {
                'Bucket': 'aadhar-kyc-hackathon',
                'Name': f"pan/{filename}"
            }
        },
        MaxLabels=10,
        Features=["GENERAL_LABELS", "IMAGE_PROPERTIES"],
        Settings={
            "GeneralLabels": {
                "LabelInclusionFilters": ["Document"]
            }
        }
    )

    detection_confidence = 0
    for label in response['Labels']:
        if label['Name'] == 'Document':
            detection_confidence = label['Confidence']

    comparison_similarity = 0
    try:
        identity = Identity.objects.get(id=identity_id)
        response = client.compare_faces(SourceImage={'S3Object': {
                                 "Bucket": "aadhar-kyc-hackathon",
                                 "Name": f"pan/{filename}"
                             }},
                             TargetImage={'S3Object': {
                                 "Bucket": "aadhar-kyc-hackathon",
                                 "Name": identity.face_image.split("amazonaws.com/")[-1]
                             }})

        comparison_similarity = response['FaceMatches'][0]['Similarity']
    except:
        return Response({'error': 'Invalid pan card'})

    pan_number = ""
    try:
        response = client.detect_text(Image={'S3Object': {
            "Bucket": "aadhar-kyc-hackathon",
            'Name': f"pan/{filename}"}})
        for text in response['TextDetections']:
            detected_text = text['DetectedText']
            pattern = re.compile("[A-Z]{3}[ABCFGHLJPTF]{1}[A-Z]{1}[0-9]{4}[A-Z]{1}")
            if pattern.match(detected_text):
                pan_number = detected_text
    except:
        return Response({'error': 'Invalid pan card'})

    if detection_confidence < 95 or comparison_similarity < 95 or pan_number == "":
        return Response({'error': 'Invalid pan card'})
    else:
        identity.pan_image = f"https://aadhar-kyc-hackathon.s3.ap-south-1.amazonaws.com/pan/{filename}"
        identity.pan_number = pan_number
        identity.save()
        return Response(IdentitySerializer(identity).data, HTTP_200_OK)

