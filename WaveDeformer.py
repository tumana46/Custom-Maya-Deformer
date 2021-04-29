import maya.OpenMayaMPx as omMPx
import maya.OpenMaya as om
import maya.cmds as mc
import sys
import math
import random

nodeName = "WaveDeformer"
nodeId = om.MTypeId(0x101fff)


class Wave(omMPx.MPxDeformerNode):
    
    mObj_Amplitude = om.MObject()
    mObj_Displace = om.MObject()
    
    def __init__(self):
        omMPx.MPxDeformerNode.__init__(self)
        
    def deform(self, dataBlock, geoIterator, matrix, geometryIndex):       
        input = omMPx.cvar.MPxGeometryFilter_input
        ## Attach a handle to input Array Attribute.
        dataHandleInputArray = dataBlock.inputArrayValue(input)
        ## Jump to particular element
        dataHandleInputArray.jumpToElement(geometryIndex)
        ## Attach a handle to specific data block
        dataHandleInputElement = dataHandleInputArray.inputValue()
        ## Reach to the child - inputGeom
        inputGeom = omMPx.cvar.MPxGeometryFilter_inputGeom
        dataHandleInputGeom = dataHandleInputElement.child(inputGeom)
        inMesh = dataHandleInputGeom.asMesh()        
        ## Envelope
        envelope = omMPx.cvar.MPxGeometryFilter_envelope
        dataHandleEnvelope = dataBlock.inputValue(envelope)
        envelopeValue = dataHandleEnvelope.asFloat()
        ## Amplitude
        dataHandleAmplitude = dataBlock.inputValue(Wave.mObj_Amplitude)
        amplitudeValue = dataHandleAmplitude.asFloat()
        ## Displace
        dataHandleDisplace = dataBlock.inputValue(Wave.mObj_Displace)
        displaceValue = dataHandleDisplace.asFloat()
        ## Getting the Normals using inMesh
        mFloatVectorArray_normal = om.MFloatVectorArray()
        mFnMesh = om.MFnMesh(inMesh)
        mFnMesh.getVertexNormals(False, mFloatVectorArray_normal, om.MSpace.kObject)
        ## Getting the Weight Value and new position value of each vertex using geoIterator
        mPointArray_meshVert = om.MPointArray()
        while ( not geoIterator.isDone()):
            pointPosition = geoIterator.position()
            weight = self.weightValue(dataBlock, geometryIndex, geoIterator.index())            
            pointPosition.x = pointPosition.x + math.sin(geoIterator.index() + displaceValue) * amplitudeValue * mFloatVectorArray_normal[geometryIndex].x * weight *envelopeValue
            pointPosition.y = pointPosition.y + math.sin(geoIterator.index() + displaceValue) * amplitudeValue * mFloatVectorArray_normal[geometryIndex].y * weight * envelopeValue            
            pointPosition.z = pointPosition.z + math.sin(geoIterator.index() + displaceValue) * amplitudeValue * mFloatVectorArray_normal[geometryIndex].z * weight * envelopeValue                              
            mPointArray_meshVert.append(pointPosition)            
            geoIterator.next()
        ## Setting the new value to each vertex
        geoIterator.setAllPositions(mPointArray_meshVert)
        
def deformerCreator():
    nodePtr = omMPx.asMPxPtr(Wave())
    return nodePtr
    
def nodeInitializer():
    ## Creating Amplitude Attributes and Setting the Attributes Keyable, Min, Max    
    mFnAttr = om.MFnNumericAttribute()
    Wave.mObj_Amplitude = mFnAttr.create("AmplitudeValue", "AmpVal", om.MFnNumericData.kFloat, 0.0)
    mFnAttr.setKeyable(1)
    mFnAttr.setMin(0.0)
    mFnAttr.setMax(1.0)    
    ## Creating Displace Attributes and Setting the Attributes Keyable, Min, Max        
    Wave.mObj_Displace = mFnAttr.create("DisplaceValue", "DispVal", om.MFnNumericData.kFloat, 0.0)
    mFnAttr.setKeyable(1)
    mFnAttr.setMin(0.0)
    mFnAttr.setMax(10.0)            
    ## Adding this two Attributes to the DeformerNode    
    Wave.addAttribute(Wave.mObj_Amplitude)
    Wave.addAttribute(Wave.mObj_Displace)        
    ## Accessing the Existing OutputGeom of the Deformer Node     
    outputGeom = omMPx.cvar.MPxGeometryFilter_outputGeom
    Wave.attributeAffects(Wave.mObj_Amplitude, outputGeom)
    Wave.attributeAffects(Wave.mObj_Displace, outputGeom)
    ## Make Deformer Paintable
    mc.makePaintable(nodeName, 'weights', attrType='multiFloat', shapeMode='deformer')
        
def initializePlugin(mObject):
    mPlugin = omMPx.MFnPlugin(mObject, "Tushar Kanti Bera", "1.0.0")
    try:
        mPlugin.registerNode(nodeName, nodeId, deformerCreator, nodeInitializer, omMPx.MPxNode.kDeformerNode)
    except:
        sys.stderr.write('Failed to register command :' + nodeName)
        
def uninitializePlugin(mObject):
    mPlugin = omMPx.MFnPluin(mObject)
    try:
        mPlugin.deregisterNode(nodeName)
    except:
        sys.stderr.write('Failed to de-register command :' + nodeName)
        
        
    









