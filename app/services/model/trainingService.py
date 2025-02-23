from sqlmodel import Session
from app.models import TrainingRun, ModelConfig
from app.services.model.definitionService import definition_service  # Placeholder
from app.config.settings import CONFIG
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

class TrainingService:
    @staticmethod
    def train_model(model_id: int, dataset_id: int, batch_size: int, num_epochs: int, learning_rate: float, session: Session):
        model_config = session.get(ModelConfig, model_id)
        dataset = session.get(Dataset, dataset_id)
        if not model_config or not dataset:
            raise ValueError("Model or dataset not found")

        # Load persisted datasets
        train_dataset = torch.load(dataset.train_dataset_path)
        val_dataset = torch.load(dataset.val_dataset_path)

        model = definition_service.define_lstm_model(
            input_size=model_config.input_size,
            hidden_layer_size=model_config.lstm_size,
            num_layers=model_config.num_lstm_layers,
            dropout=model_config.dropout
        )

        # Training setup
        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=CONFIG["training"]["scheduler_step_size"], gamma=0.1)
        train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_dataloader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

        # Training loop
        training_run = TrainingRun(
            model_config_id=model_id,
            dataset_id=dataset_id,
            batch_size=batch_size,
            num_epochs=num_epochs,
            learning_rate=learning_rate
        )
        session.add(training_run)
        session.commit()
        session.refresh(training_run)

        for epoch in range(num_epochs):
            train_loss = TrainingService.run_epoch(train_dataloader, model, criterion, optimizer, True)
            val_loss = TrainingService.run_epoch(val_dataloader, model, criterion, optimizer, False)
            scheduler.step()

        training_run.train_loss = train_loss
        training_run.val_loss = val_loss
        training_run.completed_at = torch.datetime.now()
        session.commit()

        # Save model state (simplified)
        model_state_path = f"/models/run_{training_run.id}.pth"
        torch.save(model.state_dict(), model_state_path)
        training_run.model_state_path = model_state_path
        session.commit()

        return {
            "id": training_run.id,
            "model_id": model_id,
            "dataset_id": dataset_id,
            "train_loss": train_loss,
            "val_loss": val_loss,
            "started_at": training_run.started_at,
            "completed_at": training_run.completed_at
        }

    @staticmethod
    def run_epoch(dataloader, model, criterion, optimizer, is_training):
        epoch_loss = 0
        model.train() if is_training else model.eval()
        for x, y in dataloader:
            if is_training:
                optimizer.zero_grad()
            x, y = x.to(CONFIG["training"]["device"]), y.to(CONFIG["training"]["device"])
            out = model(x)
            loss = criterion(out, y)
            if is_training:
                loss.backward()
                optimizer.step()
            epoch_loss += loss.item() / x.shape[0]
        return epoch_loss

training_service = TrainingService()