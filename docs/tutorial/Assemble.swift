import Foundation
import AVFoundation
import CoreVideo
import ImageIO
import CoreGraphics

struct Slide: Codable {
    let image: String, audio: String
    let start: Double, audioStart: Double, dur: Double
}
struct Manifest: Codable {
    let width: Int, height: Int, fps: Int, total: Double
    let slides: [Slide]
}

func die(_ m: String) -> Never { FileHandle.standardError.write((m + "\n").data(using: .utf8)!); exit(1) }

let args = CommandLine.arguments
guard args.count >= 3 else { die("usage: assemble <manifest.json> <out.mp4>") }
let manifestURL = URL(fileURLWithPath: args[1])
let outURL = URL(fileURLWithPath: args[2])
let man = try JSONDecoder().decode(Manifest.self, from: Data(contentsOf: manifestURL))
let W = man.width, H = man.height, FPS = man.fps
let TS: CMTimeScale = 600

let tmpVideo = outURL.deletingLastPathComponent().appendingPathComponent("_video_only.mp4")
for u in [tmpVideo, outURL] { try? FileManager.default.removeItem(at: u) }

// ---------------------------------------------------------------- video pass
let writer = try AVAssetWriter(outputURL: tmpVideo, fileType: .mp4)
let vSettings: [String: Any] = [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: W, AVVideoHeightKey: H,
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: 900_000,
        AVVideoMaxKeyFrameIntervalKey: FPS * 30,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoAllowFrameReorderingKey: false,
    ],
]
let vInput = AVAssetWriterInput(mediaType: .video, outputSettings: vSettings)
vInput.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(
    assetWriterInput: vInput,
    sourcePixelBufferAttributes: [
        kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB,
        kCVPixelBufferWidthKey as String: W,
        kCVPixelBufferHeightKey as String: H,
    ])
guard writer.canAdd(vInput) else { die("cannot add video input") }
writer.add(vInput)
guard writer.startWriting() else { die("startWriting failed: \(String(describing: writer.error))") }
writer.startSession(atSourceTime: .zero)

func cgImage(_ path: String) -> CGImage {
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { die("cannot read \(path)") }
    return img
}

func buffer(_ cg: CGImage) -> CVPixelBuffer {
    var pb: CVPixelBuffer?
    if let pool = adaptor.pixelBufferPool {
        CVPixelBufferPoolCreatePixelBuffer(nil, pool, &pb)
    }
    if pb == nil {
        CVPixelBufferCreate(nil, W, H, kCVPixelFormatType_32ARGB,
                            [kCVPixelBufferCGImageCompatibilityKey: true] as CFDictionary, &pb)
    }
    guard let buf = pb else { die("no pixel buffer") }
    CVPixelBufferLockBaseAddress(buf, [])
    let ctx = CGContext(data: CVPixelBufferGetBaseAddress(buf), width: W, height: H,
                        bitsPerComponent: 8, bytesPerRow: CVPixelBufferGetBytesPerRow(buf),
                        space: CGColorSpaceCreateDeviceRGB(),
                        bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue)
    ctx?.draw(cg, in: CGRect(x: 0, y: 0, width: W, height: H))
    CVPixelBufferUnlockBaseAddress(buf, [])
    return buf
}

var frame = 0
for (i, s) in man.slides.enumerated() {
    let buf = buffer(cgImage(s.image))
    let endFrame = Int((s.start + s.dur) * Double(FPS))
    while frame < endFrame {
        while !vInput.isReadyForMoreMediaData { usleep(1500) }
        let pts = CMTime(value: CMTimeValue(Double(frame) / Double(FPS) * Double(TS)), timescale: TS)
        if !adaptor.append(buf, withPresentationTime: pts) {
            die("append failed at frame \(frame): \(String(describing: writer.error))")
        }
        frame += 1
    }
    if i % 10 == 0 { print("  video: slide \(i + 1)/\(man.slides.count)") }
}
vInput.markAsFinished()
let sem = DispatchSemaphore(value: 0)
writer.finishWriting { sem.signal() }
sem.wait()
if writer.status != .completed { die("video write failed: \(String(describing: writer.error))") }
print("video track written: \(frame) frames")

// ---------------------------------------------------------------- mux audio
let comp = AVMutableComposition()
guard let vTrack = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid),
      let aTrack = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)
else { die("cannot add composition tracks") }

let vAsset = AVURLAsset(url: tmpVideo)
guard let srcV = vAsset.tracks(withMediaType: .video).first else { die("no video track") }
try vTrack.insertTimeRange(CMTimeRange(start: .zero, duration: vAsset.duration), of: srcV, at: .zero)

for s in man.slides {
    let a = AVURLAsset(url: URL(fileURLWithPath: s.audio))
    guard let srcA = a.tracks(withMediaType: .audio).first else { continue }
    let at = CMTime(value: CMTimeValue(s.audioStart * Double(TS)), timescale: TS)
    try aTrack.insertTimeRange(CMTimeRange(start: .zero, duration: a.duration), of: srcA, at: at)
}

guard let ex = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetPassthrough) else {
    die("no export session")
}
ex.outputURL = outURL
ex.outputFileType = .mp4
let sem2 = DispatchSemaphore(value: 0)
ex.exportAsynchronously { sem2.signal() }
sem2.wait()
if ex.status != .completed { die("export failed: \(String(describing: ex.error))") }
try? FileManager.default.removeItem(at: tmpVideo)
print("done: \(outURL.path)")
