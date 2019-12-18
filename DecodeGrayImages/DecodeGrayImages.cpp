#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <string>

#define DEFAULT_IMAGE_FORMAT ".jpg"
#define NUMBER_OF_BITS 10
#define mVal 15

uint16_t getGrayCode(uint16_t gray)
{
	gray ^= (gray>>8);
	gray ^= (gray>>4);
	gray ^= (gray>>2);
	gray ^= (gray>>1);
	return gray;
}

bool getIsLit(double Ld, double Lg, uint8_t pVal, uint8_t ipVal, uint8_t &isInvalid, double epsalon=5) {

	if ((Ld > Lg+epsalon) && (pVal > ipVal+epsalon)) { return true; }
	if ((Ld > Lg+epsalon) && (pVal+epsalon < ipVal)) { return false; }
	if ((pVal+epsalon < Ld) && (ipVal > Lg+epsalon)) { return false; }
	if ((pVal > Lg+epsalon) && (ipVal+epsalon < Ld)) { return true; }
	isInvalid = 255;
	return false;
}

bool load_images(std::string currentDir, std::string imgFormat, uint8_t* ph[NUMBER_OF_BITS], uint8_t* pv[NUMBER_OF_BITS], uint8_t* pih[NUMBER_OF_BITS], uint8_t* piv[NUMBER_OF_BITS],
	cv::Mat hImgs[NUMBER_OF_BITS], cv::Mat ihImgs[NUMBER_OF_BITS], cv::Mat vImgs[NUMBER_OF_BITS], cv::Mat ivImgs[NUMBER_OF_BITS]) {
	for (int i = 0; i < NUMBER_OF_BITS; i++) {
		hImgs[i] = cv::imread(currentDir + "/h" + std::to_string(i) + imgFormat, cv::IMREAD_GRAYSCALE);
		vImgs[i] = cv::imread(currentDir + "/v" + std::to_string(i) + imgFormat, cv::IMREAD_GRAYSCALE);
		ihImgs[i] = cv::imread(currentDir + "/ih" + std::to_string(i) + imgFormat, cv::IMREAD_GRAYSCALE);
		ivImgs[i] = cv::imread(currentDir + "/iv" + std::to_string(i) + imgFormat, cv::IMREAD_GRAYSCALE);
		if (hImgs[i].empty() || vImgs[i].empty() || ihImgs[i].empty() || ivImgs[i].empty()) {
			std::cout << "OpenCV could not open some files. Please ensure the following files exist." << std::endl
				<< currentDir + "/h" + std::to_string(i) + imgFormat << std::endl
				<< currentDir + "/v" + std::to_string(i) + imgFormat << std::endl
				<< currentDir + "/ih" + std::to_string(i) + imgFormat << std::endl
				<< currentDir + "/iv" + std::to_string(i) + imgFormat << std::endl;
			return false;
		}
		if (hImgs[i].isContinuous() && vImgs[i].isContinuous() && ihImgs[i].isContinuous() && ivImgs[i].isContinuous()) {
			ph[i] = hImgs[i].ptr<uint8_t>(0);
			pv[i] = vImgs[i].ptr<uint8_t>(0);
			pih[i] = ihImgs[i].ptr<uint8_t>(0);
			piv[i] = ivImgs[i].ptr<uint8_t>(0);
		}
		else {
			std::cout << "Some images werent stored continously. This should not happend and hence is not accounted for." << std::endl;
			return false;
		}
	}
	return true;
}


int main(int argc, char *argv[])
{
	std::string currentDir = ".";
	std::string imgFormat = DEFAULT_IMAGE_FORMAT;

	if (argc >= 2) {
		currentDir = std::string(argv[1]);
		std::cout << "The following directory will be used to search for the captured Images: " << currentDir << std::endl;
	} 
	if (argc > 2) {
		imgFormat = std::string(argv[2]);
		std::cout << "The following image format will be used: " << imgFormat << std::endl;
	}
	cv::Mat hImgs[NUMBER_OF_BITS], ihImgs[NUMBER_OF_BITS], vImgs[NUMBER_OF_BITS], ivImgs[NUMBER_OF_BITS];
	uint8_t *ph[NUMBER_OF_BITS], *pv[NUMBER_OF_BITS], *pih[NUMBER_OF_BITS], *piv[NUMBER_OF_BITS];

	if (!load_images(currentDir, imgFormat, ph, pv, pih, piv, hImgs, ihImgs, vImgs, ivImgs)) { return 1; }



	cv::Mat bImg, wImg;
	bImg = cv::imread(currentDir + "/b" + imgFormat, cv::IMREAD_GRAYSCALE);
	wImg = cv::imread(currentDir + "/w" + imgFormat, cv::IMREAD_GRAYSCALE);
	if (bImg.empty() || wImg.empty()) {
		std::cout << "OpenCV could not open some files. Please ensure the following files exist." << std::endl
			<< currentDir + "/b" + imgFormat << std::endl
			<< currentDir + "/w" + imgFormat << std::endl;
		return 1;
	}

	cv::Mat BinImageV(bImg.rows, bImg.cols, CV_16U);
	cv::Mat GrayImageV(bImg.rows, bImg.cols, CV_16U);
	cv::Mat InvalidImageV(bImg.rows, bImg.cols, CV_8U);

	cv::Mat BinImageH(bImg.rows, bImg.cols, CV_16U);
	cv::Mat GrayImageH(bImg.rows, bImg.cols, CV_16U);
	cv::Mat InvalidImageH(bImg.rows, bImg.cols, CV_8U);

	cv::Mat DirectImage(bImg.rows, bImg.cols, CV_8U);
	cv::Mat InDirectImage(bImg.rows, bImg.cols, CV_8U);


	uint8_t *pb, *pw, *pInvalidImageV, *pInvalidImageH, *pDirectImage, *pIndirectImage;
	uint16_t *pGrayImageV, *pGrayImageH, *pBinImageV, *pBinImageH;
	if (bImg.isContinuous() && wImg.isContinuous() && GrayImageV.isContinuous() && InvalidImageV.isContinuous()
		&& GrayImageH.isContinuous() && InvalidImageH.isContinuous() && DirectImage.isContinuous() && InDirectImage.isContinuous()
		&& BinImageH.isContinuous() && BinImageV.isContinuous()) {
		pb = bImg.ptr<uint8_t>(0);
		pw = wImg.ptr<uint8_t>(0);

		pBinImageH = BinImageH.ptr<uint16_t>(0);
		pGrayImageH = GrayImageH.ptr<uint16_t>(0);
		pInvalidImageH = InvalidImageH.ptr<uint8_t>(0);

		pBinImageV = BinImageV.ptr<uint16_t>(0);
		pGrayImageV = GrayImageV.ptr<uint16_t>(0);
		pInvalidImageV = InvalidImageV.ptr<uint8_t>(0);

		pDirectImage = DirectImage.ptr<uint8_t>(0);
		pIndirectImage = InDirectImage.ptr<uint8_t>(0);
	}
	else {
		std::cout << "Some images werent stored continously. This should not happend and hence is not accounted for." << std::endl;
		return 1;
	}
	for (int px = 0; px < bImg.size().area(); px++) {
		uint8_t iHigh = std::max(std::max(std::max(ph[9][px], pih[9][px]), std::max(pv[9][px], piv[9][px])),
			std::max(std::max(ph[8][px], pih[8][px]), std::max(pv[8][px], piv[8][px])));
		iHigh = std::max(std::max(std::max(ph[7][px], pih[7][px]), std::max(pv[7][px], piv[7][px])), iHigh);
		iHigh = std::max(std::max(std::max(ph[6][px], pih[6][px]), std::max(pv[6][px], piv[6][px])), iHigh);
		uint8_t iLow = std::min(std::min(std::min(ph[9][px], pih[9][px]), std::min(pv[9][px], piv[9][px])),
			std::min(std::min(ph[8][px], pih[8][px]), std::min(pv[8][px], piv[8][px])));
		iLow = std::min(std::min(std::min(ph[7][px], pih[7][px]), std::min(pv[7][px], piv[7][px])), iLow);
		iLow = std::min(std::min(std::min(ph[6][px], pih[6][px]), std::min(pv[6][px], piv[6][px])), iLow);

		float b_inv = (float)pw[px] / (pw[px] + pb[px]);

		double Ld = (iHigh - iLow) * b_inv;
		double Lg = 2.0 * (iHigh - Ld) * b_inv;

		pDirectImage[px] = (uint8_t)std::min(255.0, std::max(0.0, Ld));
		pIndirectImage[px] = (uint8_t)std::min(255.0, std::max(0.0, Lg));

		uint16_t grayCode = 0;

		pGrayImageV[px] = 0;
		pGrayImageH[px] = 0;

		pBinImageV[px] = 0;
		pBinImageH[px] = 0;

		if (Ld < mVal) {
			pInvalidImageV[px] = 255;
			pInvalidImageH[px] = 255;
			continue;
		}

		uint16_t valToAdd = 1;
		pInvalidImageH[px] = 0;
		for (int i = NUMBER_OF_BITS - 1; i >= 0 &&  pInvalidImageH[px] == 0; i--) {
			if (getIsLit(Ld, Lg, ph[i][px], pih[i][px], pInvalidImageH[px])) { pGrayImageH[px] += valToAdd; }
			valToAdd <<= 1;
		}
		pBinImageH[px] = getGrayCode(pGrayImageH[px]);
		valToAdd = 1;
		pInvalidImageV[px] = 0;
		for (int i = NUMBER_OF_BITS - 1; i >= 0 && pInvalidImageV[px] == 0; i--) {
			if (getIsLit(Ld, Lg, pv[i][px], piv[i][px], pInvalidImageV[px])) { pGrayImageV[px] += valToAdd; }
			valToAdd <<= 1;
		}
		pBinImageV[px] = getGrayCode(pGrayImageV[px]);


	}

	cv::imwrite(currentDir + "/out_DirectImage.tiff", DirectImage);
	cv::imwrite(currentDir + "/out_indirectImage.tiff", InDirectImage);

	cv::imwrite(currentDir + "/out_BinImageH.tiff", BinImageH);
	cv::imwrite(currentDir + "/out_GrayImageH.tiff", GrayImageH);
	cv::imwrite(currentDir + "/out_InvalidImageH.tiff", InvalidImageH);

	cv::imwrite(currentDir + "/out_BinImageV.tiff", BinImageV);
	cv::imwrite(currentDir + "/out_GrayImageV.tiff", GrayImageV);
	cv::imwrite(currentDir + "/out_InvalidImageV.tiff", InvalidImageV);
}
