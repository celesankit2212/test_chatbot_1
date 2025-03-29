#
# from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
# import torch
# import onnxruntime as ort
# from huggingface_hub import login
# import multiprocessing.resource_tracker
#
# login("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")
#
#
# MODEL_NAME = "bigcode/starcoder"
#
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)#, quantization_config=quantization_config)
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
#
# def generate_test_script(test_description):
#     prompt = f"Write a Selenium Python test script using Pytest:\n{test_description}\n\n'''python\n"
#     # response = generator(prompt, max_length=500, do_sample=True, temperature=0.7, truncation=True)
#     # return response[0]["generated_text"].split("'''python")[1].split("'''")[0].strip()
#     input_ids = tokenizer.encode(prompt, return_tensors="pt")
#     # outputs = session.run(None, {"input_ids": input_ids.numpy()})
#
#     # Export to ONNX with the required input
#     torch.onnx.export(
#         model,
#         (input_ids,),  # Example input
#         "starcoder.onnx",
#         input_names=["input_ids"],  # Define input tensor name
#         output_names=["logits"],  # Define output tensor name
#         dynamic_axes={"input_ids": {0: "batch_size", 1: "sequence_length"}, "logits": {0: "batch_size"}},
#         opset_version=14  # ONNX Opset version (ensure compatibility)
#     )
#
#     session = ort.InferenceSession("starcoder.onnx")
#     outputs = session.run(None, {"input_ids": input_ids.numpy()})
#     multiprocessing.resource_tracker.unregister('/mp-sok495t4', 'semaphore')
#     multiprocessing.resource_tracker.unregister('/mp-_yjakv4c', 'semaphore')
#     return tokenizer.decode(outputs[0][0])
#
#
#
#
# # from transformers import AutoModelForCausalLM, AutoTokenizer
# #
# # checkpoint = "bigcode/starcoder"
# # device = "cuda" # for GPU usage or "cpu" for CPU usage
# #
# # tokenizer = AutoTokenizer.from_pretrained(checkpoint)
# # model = AutoModelForCausalLM.from_pretrained(checkpoint).to(device)
# #
# # inputs = tokenizer.encode("def print_hello_world():", return_tensors="pt").to(device)
# # outputs = model.generate(inputs)
# # print(tokenizer.decode(outputs[0]))


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import onnxruntime as ort
from huggingface_hub import login


MODEL_NAME = "bigcode/starcoder"

# Load model and tokenizer
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME).to("cpu")
model.eval()  # Set to evaluation mode
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def generate_test_script(test_description):
    prompt = f"Write a Selenium Python test script using Pytest:\n{test_description}\n\n'''python\n"

    input_ids = tokenizer.encode(prompt, return_tensors="pt").to("cpu")  # Ensure CPU execution
    input_ids_numpy = input_ids.detach().cpu().numpy()  # Convert safely to NumPy

    # Export to ONNX with correct input shapes
    torch.onnx.export(
        model,
        (input_ids,),  # Input example
        "starcoder.onnx",
        input_names=["input_ids"],
        output_names=["logits"],
        dynamic_axes={"input_ids": {0: "batch_size", 1: "sequence_length"}, "logits": {0: "batch_size"}},
        opset_version=14
    )

    # Load ONNX model for inference
    session = ort.InferenceSession("starcoder.onnx")
    outputs = session.run(None, {"input_ids": input_ids_numpy})

    session._reset()  # Force cleanup
    del session  # Explicitly delete session to prevent semaphore leaks

    return tokenizer.decode(outputs[0][0])

