#include <Shlwapi.h>
#include <strmif.h>
#include <uuids.h>
#include <tchar.h>
#include "strsafe.h"
#include "vidcap.h"
#include "ksmedia.h"
#include <ksproxy.h>        // For IKsControl 
#include <Cfgmgr32.h>
#include <setupapi.h>
#include <mfapi.h>
#include <mfidl.h>
#include <Mferror.h>
#include <mfreadwrite.h>
#include <combaseapi.h>
#include "synchapi.h"
#include <guiddef.h>
#include <cstdint>  // Add this line to include the necessary header file
#include <functional>  // Add this line if you are using 'function' from the 'std' namespace
#include <Windows.h>
#include <cstdint>  // Include the necessary header for uint32_t
#include <string>   // Include the necessary header for string
#include <mutex>
#include <dbt.h>
#include "Devices.hpp"
#include "DeviceManager.hpp"


// Define HRESULT if it's not already defined
#ifndef HRESULT
typedef long HRESULT;
#endif

#define DB_LOW			1
#define DB_CRITICAL		0
#define _CRT_SECURE_NO_WARNINGS

 class Interface
  {
	  public:

		static std::unique_ptr<DeviceManager> buildDeviceManager()
		{
	#ifdef __linux__
		  return std::unique_ptr<DeviceManager>(new DeviceManager);
	#elif _WIN32
		  return std::unique_ptr<DeviceManager>(new DeviceManager);
	#endif
		}


	static std::unique_ptr<Devices> buildDevices()
	{
	#ifdef __linux__
		  return std::unique_ptr<Devices>(new Devices);
	#elif _WIN32
		  return std::unique_ptr<Devices>(new Devices);
	#endif
    }

   /* static std::unique_ptr<e_CAM512_HID> buildHID()
    {
#ifdef __linux__
      return std::unique_ptr<e_CAM512_HID>(new HID);
#elif _WIN32
      return std::unique_ptr<e_CAM512_HID>(new HID);
#endif
    }


    static std::unique_ptr<e_CAM512_UVC> buildUVC()
    {
#ifdef __linux__
      return std::unique_ptr<e_CAM512_UVC>(new UVC);
#elif _WIN32
      return std::unique_ptr<e_CAM512_UVC>(new UVC);
#endif
    }*/
  };
 
 
	typedef unsigned int uint32_t;
	unsigned char* readSampleBuffer =NULL;
	DWORD maxLength = 0, curLength = 0;
	bool v4l_retrieveFrame;
	bool Devices::v4l_streamStarted = false;
	bool Devices::v4l_stoprequested = false;
	bool Devices::v4l_gotFrame = false;
	IMFSourceReader* Devices::m_videoSourceReader = nullptr;
	std::function<void(int)> Devices::callback = NULL;
	HANDLE	Devices::m_hEvent;
	std::mutex Devices::source_reader_mutex;
	TCHAR device_path[500];
	IAMCameraControl* _pCamControl;
	IAMVideoProcAmp* _pVidProcAmp;
	IBaseFilter* _pVideoCap;
	Result is_init = Result::NotInitialized;
	Result is_opened = Result::CameraNotOpened;
	DeviceInfo device_info;
	Result e_CAM512_Error::cErrorNo;
	std::unique_ptr<DeviceManager> enumerate = Interface::buildDeviceManager();
	std::unique_ptr<Devices> cam = Interface::buildDevices();
	Result status;
	
	Result Devices::getframe(Frames* CurrFrame) 
	{
	  Result res1, res2;
	#if 1

	  if (callback == NULL) {
		  v4l_retrieveFrame = false;
		  DWORD dWait = WaitForSingleObject(m_hEvent, (100));
		  if (dWait == WAIT_TIMEOUT)
		  {
			  dbg_Print(DB_LOW, L"Device::getframe failed WAIT_TIMEOUT \n");
			  return e_CAM512_Error::setErrno(Result::Others);
		  }
	  }
	  else {
		  v4l_retrieveFrame = true;
	  }

	  if (readSampleBuffer && curLength > 0) {
		  CurrFrame->frame_data = readSampleBuffer;
		  CurrFrame->total_size = curLength;
		  CurrFrame->width = width;
		  CurrFrame->height = height;

		  if (mediaSubtype == MEDIASUBTYPE_UYVY) {
			  strcpy(CurrFrame->pixel_format, "UYVY");
		  }
		  else if (mediaSubtype == MEDIASUBTYPE_Y8) {
			  strcpy(CurrFrame->pixel_format, "Y8");
		  }
		  /*dbg_Print(DB_LOW, L" Supported Formats %s\n", format);*/
		  return Result::Ok;
	  }
	  else {
		  if (callback) {
			  v4l_retrieveFrame = false;
			  dbg_Print(DB_LOW, L"Device::getframe failed\n");
		  }
		  return e_CAM512_Error::setErrno(Result::TimeoutError);
	  }


	  if (callback) {
		  v4l_retrieveFrame = false;
	  }
#endif
	  
	  return e_CAM512_Error::setErrno(Result::Ok);
  }

	int Devices::getFramesPerSecond()
	{
		if (fpsCalculator == 0)
			fpsCalculator = clock();

		timeElapsed = ((double)(clock() - fpsCalculator) / CLOCKS_PER_SEC);
		if (timeElapsed >= 1.0)
		{
			if (callback)
				frame_count = noOfFrames;
			else
				frame_count = noOfFrames_SR;
			noOfFrames = noOfFrames_SR = 0;
			fpsCalculator = clock();
		}
			return frame_count;
	}

	void Devices::registerFrameCallback(std::function<void(int)> cb) 
	{
	  callback = cb;
	}

	
	void Devices::registerNotificationCallback(void(*cb)(int)) 
	{
	  dbg_Print(DB_LOW, L"Device::registerNotificationCallback ++\n");
	  if (cb) {
		  notification_CB = cb;

		  dbg_Print(DB_LOW, L"Device::registerNotificationCallback Success %d %d\n" , notification_CB, cb);
		  //notification_CB(22);
	  }
	  else {
		  dbg_Print(DB_LOW, L"Device::registerNotificationCallback failed\n");
	  }
	}
	
	bool Devices::open(DeviceInfo info) 
	{
		try
		{
		  HRESULT hr = E_FAIL;
		  IMFAttributes* pAttributes = NULL;
		  int i = 0; UINT32 height = 0, width = 0;
		  if (m_videoSource != NULL)
			  return false;

		  m_hEvent = CreateEvent(NULL, FALSE, FALSE, L"FrameWaitEvent");
		  if (m_hEvent == NULL)
		  {
			  return false;
		  }

		  hr = SelectVideoCaptureDevice(info, &m_videoSource);
		  if (FAILED(hr))
		  {
			  goto done;
		  }

		  return initCapture(true);
	  done:
		  Safe_Release(&pAttributes);
		  return false;
	  }
	  catch (std::bad_alloc& exception)
	  {
		  return false;

	  }
	  return false;
	}

	bool Devices::closeDevice() 
	{
	    HRESULT hr = S_FALSE;
		if (!deinitCapture()) 
		{
		  return false;
		}
		source_reader_mutex.lock();

		if (m_videoSource != NULL)
		{
			m_videoSource->Shutdown();
			Safe_Release(&m_videoSource);
			m_videoSource = NULL;
		}

		source_reader_mutex.unlock();
		  /*callback = NULL;*/ // rishap
		return true;
	}

	bool Devices::isOpened() const 
	{
	    OutputDebugString(L"isOpened ++\n");
	    return m_videoSource !=NULL;				// Checking whether the device is opened or not is done with m_videoSource
    }

	bool Devices::setFormat(uint32_t sWidth, uint32_t sHeight, TCHAR* sPixelFormat) 
	{
	  dbg_Print(DB_LOW, L"setFormat ++\r\n");
	  width = sWidth;
	  height = sHeight;

	  if (wcscmp(sPixelFormat, L"Y8") == 0) {
		  mediaSubtype = MEDIASUBTYPE_Y8;
	  }
	  else if (wcscmp(sPixelFormat, L"UYVY") == 0) {
		  mediaSubtype = MEDIASUBTYPE_UYVY;
	  }
	  deinitCapture();
	  return initCapture(false);
	}

	bool Devices::getFormat(uint32_t* Width, uint32_t* Height, TCHAR* PixelFormat) 
	{
		HRESULT hr = E_FAIL;
		IMFMediaType* pMediaType = NULL;

		if (m_videoSourceReader == NULL)
			return false;

		hr = m_videoSourceReader->GetCurrentMediaType(MF_SOURCE_READER_FIRST_VIDEO_STREAM, &pMediaType);

		if (SUCCEEDED(hr))
		{
			hr = MFGetAttributeSize(pMediaType, MF_MT_FRAME_SIZE, &width, &height);
			if (FAILED(hr))
			{
				goto failed;
			}
			hr = MFGetAttributeRatio(pMediaType, MF_MT_FRAME_RATE, &uNumerator, &uDenominator);
			if (FAILED(hr))
			{
				goto failed;
			}
			
			hr = pMediaType->GetGUID(MF_MT_SUBTYPE, &mediaSubtype);
			if (FAILED(hr))
			{
				goto failed;
			}
			*Width = width;
			*Height = height;
			if (mediaSubtype == MEDIASUBTYPE_UYVY) 
			{
				wcscpy(PixelFormat, L"UYVY");
				/* *gPixelFormat = PixFormat::PIX_FMT_UYVY;*/
			}
			  else if (mediaSubtype == MEDIASUBTYPE_Y8) 
			  {
				wcscpy(PixelFormat, L"Y8");
				//*gPixelFormat = PixFormat::PIX_FMT_Y8;
			  }
	    }
		Safe_Release(&pMediaType);
		return true;
		failed:

		Safe_Release(&pMediaType);
		return false;
	}
	
	bool Devices::stream(bool startStream)
	{
	  HRESULT hr = E_FAIL, check_hr;
	  uint32_t itr = 0;
	  if (startStream != v4l_streamStarted)
	  {

		  if (!isOpened())
		  {
			  return !startStream;
		  }
		  if (startStream) {
			  if (m_videoSourceReader != NULL)
			  {
				  hr = m_videoSourceReader->ReadSample(MF_SOURCE_READER_FIRST_VIDEO_STREAM,
					  0, NULL, NULL, NULL, NULL);

				  if (FAILED(hr))
				  {
					  return false;
				  }
				  else
				  {
					  v4l_streamStarted = true;
				  }
			  }
		  }
		  else {
			  v4l_streamStarted = false;
			  source_reader_mutex.lock();
			  if (m_videoSourceReader != NULL)
			  {
				  m_videoSourceReader->ReadSample(MF_SOURCE_READER_FIRST_VIDEO_STREAM, MF_SOURCE_READER_CONTROLF_DRAIN, NULL, NULL, NULL, NULL);
			  }

			  dbg_Print(DB_LOW, L"Before flushing ReadSample streaming OFF\r\n");

			  if(m_videoSourceReader != NULL){
				  dbg_Print(DB_LOW, L"m_videoSourceReader is NOT NULL\r\n");

				  check_hr = m_videoSourceReader->Flush(MF_SOURCE_READER_ALL_STREAMS);
				  if(check_hr == S_OK)
					  dbg_Print(DB_LOW, L"Flush succeded\r\n");
				  else
				  {
					  dbg_Print(DB_LOW, L"Flush Failed\r\n");
					  if(check_hr == MF_E_NOTACCEPTING)
						  dbg_Print(DB_LOW, L"Flush Failed error is MF_E_NOTACCEPTING\r\n");
				  }

			  }else
				  dbg_Print(DB_LOW, L"m_videoSourceReader is NULL\r\n");

			  check_hr = m_videoSource->Stop();
			  if (check_hr == S_OK)
				  dbg_Print(DB_LOW, L"Stop succeded\r\n");
			  else
			  {
				  dbg_Print(DB_LOW, L"stop Failed\r\n");
				  if (check_hr == MF_E_NOTACCEPTING)
					  dbg_Print(DB_LOW, L"stop Failed error is MF_E_NOTACCEPTING\r\n");
			  }

			  source_reader_mutex.unlock();
			  return !startStream;
		  }
	  }
	  return startStream;
	}
	
	bool Devices::try_format()
	{
		  IMFMediaType* pSrcOutMediaType = NULL;
		  HRESULT hr = E_FAIL,cr;
		  hr = MFCreateMediaType(&pSrcOutMediaType);
		  if (FAILED(hr))
		  {
			  dbg_Print(DB_LOW, L"CSetCameraProperty::MFCreateMediaType failed\r\n");
			  goto done;
		  }

		  if (pSrcOutMediaType != NULL)
		  {
			  hr = pSrcOutMediaType->SetGUID(MF_MT_MAJOR_TYPE, MFMediaType_Video);
			  if (FAILED(hr))
			  {
				  dbg_Print(DB_LOW, L"CSetCameraProperty::SetGUID MAJOR_TYPE failed\r\n");
				  goto done;
			  }
		  }
		  else
			  goto done;
		  if (pSrcOutMediaType != NULL)
		  {
			  hr = pSrcOutMediaType->SetGUID(MF_MT_SUBTYPE, mediaSubtype);
			  if (FAILED(hr))
			  {
				  dbg_Print(DB_LOW, L"CSetCameraProperty::SetGUID SUBTYPE failed\r\n");
				  goto done;
			  }
		  }
		  else
			  goto done;

		  hr = MFSetAttributeSize(pSrcOutMediaType, MF_MT_FRAME_SIZE, width, height);
		  if (FAILED(hr))
		  {
			  dbg_Print(DB_LOW, L"CSetCameraProperty::MFSetAttributeSize failed\r\n");
			  goto done;
		  }

		  if (m_videoSourceReader != NULL)
		  {
			  hr = m_videoSourceReader->SetCurrentMediaType(0, NULL, pSrcOutMediaType);
			  if (FAILED(hr))
			  {
				  dbg_Print(DB_LOW, L"CSetCameraProperty::SetCurrentMediaType failed\r\n");
				  goto done;
			  }
		  }
		  else
			  goto done;
		  if (pSrcOutMediaType != NULL)
		  {
			  Safe_Release(&pSrcOutMediaType);
		  }
		  return true;
	  done:
		  if (pSrcOutMediaType != NULL)
		  {
			  Safe_Release(&pSrcOutMediaType);
		  }
		  return false;
  }

	HRESULT Devices::SelectVideoCaptureDevice(DeviceInfo info, IMFMediaSource** ppVideoSource)
	{
	  try
	  {
		  //Changed by Abishek
		  // Converted from char to w_char due to change in SDK for Python compatibility
		  
		  size_t ret_count;
		  if (mbstowcs_s(&ret_count, device_path, 500, info.devicePath, 500) == 0)
		  {
			  dbg_Print(DB_CRITICAL, L"\nmbstowcs_s success");

		  }

		  // Select a suitable video capture device and initialize video source object

		  HRESULT hr;

		  IMFAttributes* pVideoSrcAttribute = 0;
		  IMFActivate** ppActivateArray = 0;
		  UINT32 uNoOfDevice = 0;

		  UINT32 i;
		  int iSelectedVidCaptureDev = -1;
		  IMFMediaSource* pVideoSource = NULL;

		  LPWSTR lpDevicePath = 0, lpActualDevicePath = device_path;
		  TCHAR tzExtractPath[100], * tzRemoveGUIDStr;
		  TCHAR tzDeviceExtractPath[100];

		  *ppVideoSource = 0;

		  // Create a container for enumeration criteria
		  hr = MFCreateAttributes(&pVideoSrcAttribute, 1);
		  if (FAILED(hr))
		  {
			  dbg_Print(DB_LOW, L"SelectVideoCaptureDevice::MFCreateAttributes failed\r\n");
			  goto done;
		  }

		  // List video capture devices
		  if (pVideoSrcAttribute != NULL)
		  {
			  hr = pVideoSrcAttribute->SetGUID(MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE, MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE_VIDCAP_GUID);
			  if (FAILED(hr))
			  {
				  dbg_Print(DB_LOW, L"SelectVideoCaptureDevice::SetGUID failed\r\n");
				  goto done;
			  }
		  }
		  else
			  goto done;

		  hr = MFEnumDeviceSources(pVideoSrcAttribute, &ppActivateArray, &uNoOfDevice);
		  if (FAILED(hr))
		  {
			  dbg_Print(DB_LOW, L"SelectVideoCaptureDevice::MFEnumDeviceSources failed\r\n");
			  goto done;
		  }

		  // Release attributes
		  if (pVideoSrcAttribute != NULL)
		  {
			  Safe_Release(&pVideoSrcAttribute);
		  }

		  // List names
		  for (i = 0; i < uNoOfDevice; i++)
		  {
			  if (ppActivateArray[i] != NULL)
			  {
				  hr = ppActivateArray[i]->GetAllocatedString(MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE_VIDCAP_SYMBOLIC_LINK, &lpDevicePath, 0);
				  if (FAILED(hr))
				  {
					  dbg_Print(DB_LOW, L"SelectVideoCaptureDevice::GetAllocatedString failed\r\n");
					  goto done;
				  }
			  }
			  else
				  goto done;
			  dbg_Print(DB_CRITICAL, L"lpDevicePath:%s\n", lpDevicePath);

			  tzRemoveGUIDStr = wcschr(lpDevicePath, L'{');
			  wcsncpy_s(tzExtractPath, lpDevicePath, (tzRemoveGUIDStr - lpDevicePath));
			  dbg_Print(DB_CRITICAL, L"tzExtractPath:%s\n", tzExtractPath);

			  tzRemoveGUIDStr = wcschr(device_path, L'{');
			  wcsncpy_s(tzDeviceExtractPath, lpActualDevicePath, (tzRemoveGUIDStr - device_path));
			  dbg_Print(DB_CRITICAL, L"tzDeviceExtractPath:%s\n", tzDeviceExtractPath);


			  if (!wcscmp(wcsupr(tzExtractPath), (tzDeviceExtractPath)))
			  {
				  iSelectedVidCaptureDev = i;
				  break;
			  }
			  else
			  {
				  iSelectedVidCaptureDev = -1;
			  }

			  CoTaskMemFree(lpDevicePath);
		  }
		  dbg_Print(DB_CRITICAL, L"iSelectedVidCaptureDev:%d\n", iSelectedVidCaptureDev);
		  // No camera
		  if ((uNoOfDevice == 0) || (iSelectedVidCaptureDev == -1))
			  goto done;

		  if (ppActivateArray[iSelectedVidCaptureDev] != NULL)
		  {
			  hr = ppActivateArray[iSelectedVidCaptureDev]->GetAllocatedString(MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE_VIDCAP_SYMBOLIC_LINK, &lpDevicePath, 0);
			  if (FAILED(hr))
			  {
				  dbg_Print(DB_LOW, L"SelectVideoCaptureDevice::GetAllocatedString failed\r\n");
				  goto done;
			  }
		  }
		  else
			  goto done;


		  // Get media source for selected capture device
		  if (ppActivateArray[iSelectedVidCaptureDev] != NULL)
		  {
			  hr = ppActivateArray[iSelectedVidCaptureDev]->ActivateObject(IID_IMFMediaSourceEx, (void**)&pVideoSource);
			  if (FAILED(hr))
			  {
				  dbg_Print(DB_LOW, L"SelectVideoCaptureDevice::ActivateObject failed\r\n");
				  goto done;
			  }
		  }
		  else
			  goto done;

		  if (pVideoSource != NULL)
		  {
			  dbg_Print(DB_CRITICAL, L"ppVideoSource created\n");
			  *ppVideoSource = pVideoSource;
			  (*ppVideoSource)->AddRef();
		  }

	  done:
		  // Release array elements
		  for (i = 0; i < uNoOfDevice; i++)
		  {
			  if (ppActivateArray[i] != NULL)
			  {
				  Safe_Release(&ppActivateArray[i]);
			  }
		  }

		  CoTaskMemFree(ppActivateArray);
		  Safe_Release(&pVideoSource);
		  dbg_Print(DB_CRITICAL, L"SelectVideoCaptureDevice finished\n");
		  return hr;

	  }
	  catch (...)
	  {
		  return E_FAIL;
	  }
  }
	bool Devices::initCapture(bool FirstCapture) 
	{
		//dbg_Print(DB_LOW, L"initCapture ++\n");
		HRESULT hr = E_FAIL;
		  IMFAttributes* pAttributes = NULL;
		  if (!isOpened()) {
			//dbg_Print(DB_LOW, L"isOpened False\n");
			  return false;
		  }

		  hr = MFCreateAttributes(&pAttributes, 1);
		  if (FAILED(hr))
		  {
				//dbg_Print(DB_LOW, L"MFCreateAttributes Failed\n");
				goto done;
		  }
		  //dbg_Print(DB_CRITICAL, L"MFCreateAttributes success\n");

		  hr = pAttributes->SetUINT32(MF_READWRITE_DISABLE_CONVERTERS, TRUE);
		  if (FAILED(hr))
		  {
			  //dbg_Print(DB_LOW, L"SetUINT32 Failed\n");
			  goto done;
		  }
		  //dbg_Print(DB_CRITICAL, L"SetUINT32 success\n");

		  hr = pAttributes->SetGUID(
			  MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE,
			  MF_DEVSOURCE_ATTRIBUTE_SOURCE_TYPE_VIDCAP_GUID);
		  if (FAILED(hr))
		  {
			  //dbg_Print(DB_LOW, L"CInit::SetGUID Failed\r\n");
			  goto done;
		  }
		  //dbg_Print(DB_CRITICAL, L"CInit::SetGUID success\r\n");

		  hr = pAttributes->SetUnknown(MF_SOURCE_READER_ASYNC_CALLBACK, (IMFSourceReaderCallback*)this);
		  if (FAILED(hr))
		  {
			  //dbg_Print(DB_LOW, L"CInit::SetUnknown failed\r\n");
			  goto done;
		  }
		  //dbg_Print(DB_CRITICAL, L"CInit::SetUnknown success\r\n");
		  if (m_videoSource == 0) {
			  //dbg_Print(DB_LOW, L"CInit::m_videoSource is zero\r\n");

		  }

		  hr = MFCreateSourceReaderFromMediaSource(m_videoSource, pAttributes, &m_videoSourceReader);
		  if (FAILED(hr))
		  {
			  //dbg_Print(DB_LOW, L"CInit::MFCreateSourceReaderFromMediaSource failed %s \r\n", hr);
			  goto done;
		  }
		  //dbg_Print(DB_CRITICAL, L"CInit::MFCreateSourceReaderFromMediaSource success \r\n");
		  Safe_Release(&pAttributes);

		  if (FirstCapture) {
			  getFormat(&width, &height, &format);
		  }
		  else {
			  if (!try_format()) {
				  //dbg_Print(DB_LOW, L"CInit::try_format failed\r\n");
				  return false;
			  }
		  }

		  if (!stream(true)) {
			  return false;
		  }
		  else {
			  v4l_stoprequested = false;
			  if (m_videoSourceReader )
			  {
				  hr = m_videoSourceReader->ReadSample(MF_SOURCE_READER_FIRST_VIDEO_STREAM,
					  0, NULL, NULL, NULL, NULL);
			  }
		  }
		  return true;
	  done:
		  Safe_Release(&pAttributes);
		  return false;
  }
  
	bool Devices::deinitCapture() 
	{
		if (v4l_streamStarted) {
		  v4l_stoprequested = true;
		  if (!stream(false)) {
			  return false;
		  }
		  else 
		  {
				mtx.lock();
				if (readSampleBuffer) {
					free(readSampleBuffer);
					readSampleBuffer = NULL;
				}
				mtx.unlock();
				//frame->setupFrame(NULL, 0);
				curLength = 0;
		  }
		}

	  return true;
	}

	int Devices::getCameraProperties(uint32_t Index, ImageProperty *imgProperties)
	{
	  try
	  {
		  HRESULT hr = S_OK;
		  IMFMediaType *pMediaType = NULL;
		  GUID mediaSubType;
		  int iValidformatCounter = 0, supportedFormats = 0;
		  UINT32 width = 0, height = 0, numeratorFPS = 0, denominatorFPS = 0;
		  bool isValidFormat = true;
		  if (m_videoSourceReader == NULL)
			  return 0;
		  int Cnt = 0;

			  isValidFormat = true;
			  hr = m_videoSourceReader->GetNativeMediaType(0, Index, &pMediaType);
			  if (SUCCEEDED(hr))
			  {
				  hr = MFGetAttributeSize(pMediaType, MF_MT_FRAME_SIZE, &width, &height);
				  if (FAILED(hr))
				  {
					  goto failed;
				  }
				  hr = MFGetAttributeRatio(pMediaType, MF_MT_FRAME_RATE, &numeratorFPS, &denominatorFPS);
				  if (FAILED(hr))
				  {
					  goto failed;
				  }
				  hr = pMediaType->GetGUID(MF_MT_SUBTYPE, &mediaSubType);;
				  if (FAILED(hr))
				  {
					  goto failed;
				  }
					  if (mediaSubType == MFVideoFormat_MJPG)
					  {
						  strcpy(imgProperties[0].Compression, "MJPG");
					  }
					  else if (mediaSubType == MFVideoFormat_UYVY)
					  {
						  strcpy(imgProperties[0].Compression, "UYVY");
					  }
					  else if (mediaSubType == MFVideoFormat_YVYU)
					  {
						  strcpy(imgProperties[0].Compression, "YVYU");
					  }
					  else if (mediaSubType == MFVideoFormat_YUY2)
					  {
						  strcpy(imgProperties[0].Compression, "YUY2");
					  }
					  else if (mediaSubType == MEDIASUBTYPE_Y8)
					  {
						  strcpy(imgProperties[0].Compression,"Y8");
					  }
					  else if (mediaSubType == MEDIASUBTYPE_Y16)
					  {
						  strcpy(imgProperties[0].Compression, "Y16");
						 
					  }
					  else if (mediaSubType == MFVideoFormat_H264)
					  {
						  strcpy(imgProperties[0].Compression, "H264");
						 
					  }
					  else
					  {
						  isValidFormat = false;
					  }
					  if (isValidFormat)
					  {
						  imgProperties[0].width = width;
						  imgProperties[0].height = height;
						  imgProperties[0].fps = numeratorFPS / denominatorFPS;
						  supportedFormats++;
						  dbg_Print(DB_LOW, L" Supported Formats index %d %d %d x %d %d %c \n", Index, supportedFormats, width, height, imgProperties[0].fps, imgProperties[0].Compression[0]);
						  //DebugMessage(DEBUGLOG_ENABLED, L"%d - width :  %d , height : %d , FPS : %d , %s \r\n", supportedFormats, width, height, numeratorFPS / denominatorFPS, imgProperties[supportedFormats].Compression);
					  }
					  

				  }
				
			  
	  failed:
		  Safe_Release(&pMediaType);
		  if (supportedFormats > 0)
		  {
			  return supportedFormats;
		  }
		  else
		  {
			  return 0;
		  }
	  }
	  catch (...)
	  {
		  //DebugMessage(1, L"CMFSourceReader::CGetCameraProperties Exception \r\n");
		  return -1;
	  }
  }
	
	STDMETHODIMP Devices::QueryInterface(REFIID iid, void** ppv)
	{
	  static const QITAB qit[] =
	  {
		  QITABENT(Devices, IMFSourceReaderCallback),
		  { 0 },
	  };
	  return QISearch(this, qit, iid, ppv);
	}
	
	HRESULT	queryUvcInterface()
	{
			HRESULT hr = E_FAIL;
		try
		{

			if (_pVideoCap == NULL)
				return hr;

			hr = _pVideoCap->QueryInterface(IID_IAMCameraControl, (void**)&(_pCamControl));
			if (FAILED(hr))
			{
				return hr;
			}

			hr = _pVideoCap->QueryInterface(IID_IAMVideoProcAmp, (void**)&(_pVidProcAmp));
			if (FAILED(hr))
			{
				return hr;
			}
		}
		catch (...)
		{
			return E_FAIL;
		}
		return hr;
	}

	bool getUVCControl( uint32_t ControlID, UVCProp* ControlValue)
	{
		  try
		  {
			  HRESULT hr = E_FAIL;
			  bool bProcAmpSelected = true;
			  bool getAutoManual = false;
			  long lMax, lMin, lDefault, lStepping, lCurValue;
			  long lCapsFlag = CameraControl_Flags_Manual;
			  long lProperty = 0;
			  long automanual = CameraControl_Flags_Manual;
			  if ((_pCamControl == NULL) || (_pVidProcAmp == NULL))
			  {
				  if (FAILED(queryUvcInterface()))
				  {
					  //return e_CAM512_Error::setErrno(Result::NoPropertyValueGet);
					  return true;
				  }
			  }
			  ControlValue->id = ControlID;
			  lProperty = ControlID;
			  if (ControlID > 13) {
				  lProperty -= 14;
				  bProcAmpSelected = false; 
			  }

			  if (bProcAmpSelected)
			  {
				  hr = _pVidProcAmp->Get(lProperty, &lCurValue, &lCapsFlag);
				  if (FAILED(hr))
				  {
					  return false;
					 // return e_CAM512_Error::setErrno(Result::NoPropertyValueGet);
				  }
				  automanual = lCapsFlag;
				  if (lProperty == VideoProcAmp_WhiteBalance && getAutoManual)
				  {
					  //PrintMessages(DB_LOW, L"1.whitebalance auto:%d\n",lCapsFlag);
				  }
				  hr = _pVidProcAmp->GetRange(lProperty, &lMin, &lMax, &lStepping, &lDefault, &lCapsFlag);
				  if (FAILED(hr))
				  {
					  return false;
					 // return e_CAM512_Error::setErrno(Result::NoPropertyValueGet);
				  }
				  
				  if (lProperty == VideoProcAmp_WhiteBalance && getAutoManual)
				  {
					  //PrintMessages(DB_LOW, L"2.whitebalance auto:%d\n", lCapsFlag);
				  }
			  }
			  else
			  {
				  hr = _pCamControl->Get(lProperty, &lCurValue, &lCapsFlag);
				  if (FAILED(hr))
				  {
					  return false;
					 // return e_CAM512_Error::setErrno(Result::NoPropertyValueGet);
				  }
				  automanual = lCapsFlag;
				  hr = _pCamControl->GetRange(lProperty, &lMin, &lMax, &lStepping, &lDefault, &lCapsFlag);
				  if (FAILED(hr))
				  {
					  return false;
					  //return e_CAM512_Error::setErrno(Result::NoPropertyValueGet);
				  }
			  }

			  if (getAutoManual) {

				  if (automanual == CameraControl_Flags_Auto)
				  {
					  if (lProperty == VideoProcamp_WhiteBalance) 
					  {
						  ControlValue->cur = 1;
					  }
					  else if (lProperty == Cameracontrol_Exposure)
					  {
						  ControlValue->cur = 0;
					  }
				  }
				  else if(automanual == CameraControl_Flags_Manual){
					  if (lProperty == VideoProcamp_WhiteBalance)
					  {
						  ControlValue->cur = 0;
					  }
					  else if (lProperty == Cameracontrol_Exposure)
					  {
						  ControlValue->cur = 1;
					  }
				  }
			  }
			  else {
				  ControlValue->cur = lCurValue;
				  ControlValue->max = lMax;
				  ControlValue->min = lMin;
				  ControlValue->step = lStepping;
				  ControlValue->default_val = lDefault;
				  ControlValue->automan = automanual;
			  }
			  //return e_CAM512_Error::e_CAM512_Error::setErrno(Result::Ok);
			  return true;
		  }
		  catch (...)
		  { 
			 // return e_CAM512_Error::setErrno(Result::NoPropertyValueGet);
			 return false;
		  }
	  }

	bool setUVCControl( uint32_t ControlID, int32_t ControlValue,bool AutoMode)
	{
		  try
		  {
			  bool bProcAmpSelected = true;
			  bool setAutoManual = false;
			  long lProperty = 0;
			  long lCapsFlag;
			  long sCurValue;
			  UVCProp gCurValue;
			  HRESULT hr = E_FAIL;
			  if ((_pCamControl == NULL) || (_pVidProcAmp == NULL))
				  return false;
				  //return e_CAM512_Error::setErrno(Result::NoPropertyValueSet);

			  switch (ControlID) {
			  case VideoProcamp_Brightness:
				  lProperty = VideoProcamp_Brightness;
				  break;
			  case VideoProcamp_Contrast:
				  lProperty = VideoProcamp_Contrast;
				  break;
			  case VideoProcamp_Saturation:
				  lProperty = VideoProcamp_Saturation;
				  break;
			  case VideoProcamp_WhiteBalance:
				  lProperty = VideoProcamp_WhiteBalance;
				  gCurValue.id = VideoProcamp_WhiteBalance;
				  break;
			  case VideoProcamp_Gamma:
				  lProperty = VideoProcamp_Gamma;
				  break;
			  case VideoProcamp_Gain:
				  lProperty = VideoProcamp_Gain;
				  break;
			  case KSPROPERTY_VIDEOPROCAMP_POWERLINE_FREQUENCY:
				  lProperty = KSPROPERTY_VIDEOPROCAMP_POWERLINE_FREQUENCY;
				  break;
			  case VideoProcamp_Sharpness:
				  lProperty = VideoProcamp_Sharpness;
				  break;
			  case Cameracontrol_Exposure:
				  lProperty = CameraControl_Exposure;
				  bProcAmpSelected = false;
				  gCurValue.id = CameraControl_Exposure;
				  break;
			  }
			  setAutoManual = AutoMode;
			  if (setAutoManual) {

				  if (ControlValue) {
					  if (lProperty == VideoProcamp_WhiteBalance)
					  {
						  lCapsFlag = CameraControl_Flags_Auto;
					  }
					  else if (lProperty == CameraControl_Exposure)
					  {
						  lCapsFlag = CameraControl_Flags_Manual;
					  }
				  }
				  else {
					  if (lProperty == VideoProcamp_WhiteBalance)
					  {
						  lCapsFlag = CameraControl_Flags_Manual;
					  }
					  else if (lProperty == CameraControl_Exposure)
					  {
						  lCapsFlag = CameraControl_Flags_Auto;
					  }
				  }
				  getUVCControl(gCurValue.id, &gCurValue);
				  sCurValue = gCurValue.cur;
			  }
			  else {
				  lCapsFlag = CameraControl_Flags_Manual;
				  sCurValue = ControlValue;
			  }
			  if (bProcAmpSelected)
			  {
				  hr = _pVidProcAmp->Set(lProperty, sCurValue, lCapsFlag);
				  if (FAILED(hr))
				  {
					  return false;
					  //return e_CAM512_Error::setErrno(Result::NoPropertyValueSet);
				  }
			  }
			  else
			  {
				  hr = _pCamControl->Set(lProperty, sCurValue, lCapsFlag);
				  if (FAILED(hr))
				  {
					  return false;
					  //return e_CAM512_Error::setErrno(Result::NoPropertyValueSet);
				  }
			  }
			 // return e_CAM512_Error::e_CAM512_Error::setErrno(Result::Ok);
			 return true;
		  }
		  catch (...)
		  {
			 // return e_CAM512_Error::setErrno(Result::NoPropertyValueSet);
			 return false;
		  }
	}
	
    STDMETHODIMP Devices::OnFlush(DWORD)
    {
		return S_OK;
    }
	
    STDMETHODIMP Devices::OnEvent(DWORD, IMFMediaEvent*)
    {
	    return S_OK;
    }
	
	 HRESULT Devices::OnReadSample(
	  HRESULT hrStatus,
	  DWORD  dwStreamIndex,
	  DWORD  dwStreamFlags,
	  LONGLONG  llTimestamp,
	  IMFSample* pSample      // Can be NULL
  )
	{
	  HRESULT hr = S_FALSE;
	  IMFMediaBuffer* media_buffer = NULL;

	 
	  if (SUCCEEDED(hrStatus))
	  {
		  if (pSample)
		  {
			  if (v4l_streamStarted) {
				  hr = pSample->GetBufferByIndex(0, &media_buffer);
				  if (SUCCEEDED(hr))
				  {
						  BYTE* buf = NULL;
						  if (SUCCEEDED(hr = media_buffer->Lock(&buf, &maxLength, &curLength)))
						  {
							  if (!v4l_retrieveFrame) {


								  mtx.lock();
								  if (!readSampleBuffer && curLength >0) {
									  readSampleBuffer = (unsigned char*)malloc(curLength);
									  if (!readSampleBuffer)
									  {
										  dbg_Print(DB_LOW, L"OnReadSample::memory allocation failed\r\n");
									  }
								  }

								  if (readSampleBuffer) {
									memcpy(readSampleBuffer,buf, curLength);
									noOfFrames_SR++;
									frame_recieved = true;
								  }
								  if (callback) {
									  callback(1);
								  }
								  mtx.unlock();
								  media_buffer->Unlock();

								  Safe_Release(&media_buffer);

								  if (callback == NULL && m_hEvent) {
									  v4l_retrieveFrame = true;
								      SetEvent(m_hEvent);
								  }

							  }
							  else {
								  media_buffer->Unlock();
								  Safe_Release(&media_buffer);
								  media_buffer = NULL;

							  }

						  }
						  else {
							  Safe_Release(&media_buffer);
							  media_buffer = NULL;
							  dbg_Print(DB_LOW, L"OnReadSample:: IMFMediaBuffer Lock failed\r\n");

						  }
				  }
				  else
				  {
					  Safe_Release(&media_buffer);
					  media_buffer = NULL;
					  dbg_Print(DB_LOW, L"OnReadSample:: GetBufferByIndex frame\r\n");
				  }
				  if (SUCCEEDED(hr))
				  {
					  if (m_videoSourceReader != NULL)
					  {

						  hr = m_videoSourceReader->ReadSample(
							  MF_SOURCE_READER_FIRST_VIDEO_STREAM,				//Index of the video stream to get frames from it
							  0,
							  NULL,    // actual
							  NULL,   // flags
							  NULL,   // timestamp
							  NULL    // sample
						  );
						  if (FAILED(hr))
						  {
							  dbg_Print(DB_LOW, L"OnReadSample::ReadSample second failed\r\n");
						  }
					  }
				  }
				  else
					  dbg_Print(DB_LOW, L"OnReadSample:: requesting next frame pass failed\r\n");

			  }

		  }
		  else
		  {
			  if (m_videoSourceReader != NULL)
			  {
				  dbg_Print(DB_LOW, L"OnReadSample::pSample is failed\r\n");
				  hr = m_videoSourceReader->ReadSample(
					  MF_SOURCE_READER_FIRST_VIDEO_STREAM,				//Index of the video stream to get frames from it
					  0,
					  NULL,    // actual
					  NULL,   // flags
					  NULL,   // timestamp
					  NULL    // sample
				  );
				  if (FAILED(hr))
				  {
					  dbg_Print(DB_LOW, L"OnReadSample::ReadSample second failed\r\n");
				  }
			  }
			  dbg_Print(DB_LOW, L"OnReadSample::pSample is failed\r\n");
		  }
	  }
	  else
	  {
		  if (m_videoSourceReader != NULL)
		  {

			  hr = m_videoSourceReader->ReadSample(
				  MF_SOURCE_READER_FIRST_VIDEO_STREAM,				//Index of the video stream to get frames from it
				  0,
				  NULL,    // actual
				  NULL,   // flags
				  NULL,   // timestamp
				  NULL    // sample
			  );
			  if (FAILED(hr))
			  {
				  dbg_Print(DB_LOW, L"OnReadSample::ReadSample second failed\r\n");
			  }
		  }
		  dbg_Print(DB_LOW, L"OnReadSample::hrStatus is failed\r\n");
	  }

  done:

	  return S_OK;
  }
	
	STDMETHODIMP_(ULONG) Devices::AddRef()
	{
		return InterlockedIncrement(&m_nRefCount);
	}

	STDMETHODIMP_(ULONG) Devices::Release()
	{
		ULONG uCount = InterlockedDecrement(&m_nRefCount);
		if (uCount == 0)
		{
			delete this;
		}
		return uCount;
	}

	Result Close_Device()
	{
		OutputDebugString(L"CloseDevice ++ \n");
		if (is_opened == Result::Ok) {
			OutputDebugString(L"CloseDevice :: is_opened == Result::Ok \n");
			if (cam->isOpened()) {
				cam->closeDevice();

			}
			else
				is_opened = e_CAM512_Error::setErrno(Result::CameraNotOpened);
		}
		return is_opened;
	}
 
	Result OpenDevice(uint32_t deviceIndex)
	{
		DeviceInfo info;
		uint32_t cDeviceNum;
		uint16_t cDepthRange = -1;
		DataMode cDataMode = DataMode::ModeUnknown;
		if (is_init == Result::NotInitialized) {
			return is_init;
		}
		
		
		if (!(enumerate->isValidIndex(deviceIndex))) 
		{
			return status;
		}

		cDeviceNum = deviceIndex;
		enumerate->getDevNodeNumber(&cDeviceNum);


		Close_Device();
		if (!(enumerate->getDeviceInfo(deviceIndex, &info))) {
			goto Failure;
		}
		device_info = info;
		/* if (hid->openHID(&info) < 0) {
			goto Failure;
		}
		if (uvc->_openUVC(info) < 0) {
			goto Failure;
		} */
		

		if (cam)
		{
			cam->open(info);
		}
		else
		{
			goto Failure;
		}
		if (!cam->isOpened()) {
			goto Failure;
		}
		else {

			is_opened = Result::Ok;
		}
		return Result::Ok;
	 Failure:
		is_opened = Close_Device();
		return is_opened; 
	}
	
	//Wrapper for python
	
	py::tuple Cam::OpenDeviceWrapper(uint32_t deviceIndex) 
	{
		uint32_t result = OpenDevice(deviceIndex);
		return py::make_tuple(result);
	}
	
	py::tuple Cam::getFormatWrapper() 
	{
		uint32_t gWidth, gHeight;
		TCHAR gPixelFormat[256];  // Adjust the size as per your requirement
		
		bool result = cam->getFormat(&gWidth, &gHeight, gPixelFormat);
		return py::make_tuple(result, gWidth, gHeight, gPixelFormat);
	}
	
	py::tuple Cam::getCameraPropertiesWrapper(uint32_t Index) 
	{
		ImageProperty imgProperties;
		int result = cam->getCameraProperties(Index, &imgProperties);
		return py::make_tuple(result, imgProperties);
	}
	
	py::tuple Cam::getUVCControlWrapper(uint32_t ControlID, UVCProp* ControlValue) 
	{
		bool result = getUVCControl(ControlID, ControlValue);
		return py::make_tuple(result, *ControlValue);
	}
	
	py::tuple Cam::setUVCControlWrapper(uint32_t ControlID, int32_t ControlValue, bool AutoMode) 
	{
    bool result = setUVCControl(ControlID, ControlValue, AutoMode);
    return py::make_tuple(result);
	}
	py::tuple Cam::setFormatWrapper(uint32_t sWidth, uint32_t sHeight, const TCHAR* sPixelFormat) {
    bool result = cam->setFormat(sWidth, sHeight, const_cast<TCHAR*>(sPixelFormat));
    return py::make_tuple(result);
}
	
	py::tuple Cam::getframeWrapper() 
	{
		Frames currFrame;
		Result result = cam->getframe(&currFrame);
		return py::make_tuple(currFrame, result);
	}
	
	py::tuple Cam::closeDeviceWrapper() 
	{
		bool result = Close_Device();
		return py::make_tuple(result);
	}
	
	PYBIND11_MODULE(pyeCam, m) 
	{
		py::class_<DeviceManager>(m, "DeviceManager")
			.def(py::init<>())
			.def("getDeviceCount", &DeviceManager::getDeviceCountWrapper, "Get the device count")
			.def("getDeviceInfo", &DeviceManager::getDeviceInfoWrapper, py::arg("deviceIndex"), "Get device information");
			
		py::class_<Cam>(m, "Cam")
			.def(py::init<>())
			.def("OpenDevice", &Cam::OpenDeviceWrapper, "Open a device")
			.def("setFormat", &Cam::setFormatWrapper, "Set the device format")
			.def("getFormat", &Cam::getFormatWrapper, "Get the format information")
			.def("getCameraProperties", &Cam::getCameraPropertiesWrapper, "Get camera properties")
			.def("closeDevice", &Cam::closeDeviceWrapper, "Close the device")
			.def("getframe", &Cam::getframeWrapper, "Get the current frame")
			.def("getUVCControl", &Cam::getUVCControlWrapper, "Get UVC control")
			.def("setUVCControl", &Cam::setUVCControlWrapper, "Set UVC control");
	}



